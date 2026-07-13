from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any
import json
from fastapi.responses import StreamingResponse
from groq import RateLimitError, InternalServerError
import random
import time
import re
import yaml
from pathlib import Path


load_dotenv() # This loads the hidden key from the .env file safely

app = FastAPI(title="BhagvadGPT API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

print("Initializing BhagvadGPT Backend...")

# API Key Rotation Setup - Keys from DIFFERENT accounts for true 5x capacity
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY1"),
    os.getenv("GROQ_API_KEY2"), 
    os.getenv("GROQ_API_KEY3"),
    os.getenv("GROQ_API_KEY4"),
    os.getenv("GROQ_API_KEY5"), 
]

# Filter out None values in case .env key is missing
GROQ_API_KEYS = [key for key in GROQ_API_KEYS if key]

# Track key usage and failures
key_stats = {key: {"uses": 0, "failures": 0, "last_failure": 0} for key in GROQ_API_KEYS}
current_key_index = 0

def get_next_api_key():
    """Get the next API key in rotation, skipping recently failed keys"""
    global current_key_index
    
    current_time = time.time()
    available_keys = []
    
    # Find keys that haven't failed recently (within last 60 seconds)
    for i, key in enumerate(GROQ_API_KEYS):
        if current_time - key_stats[key]["last_failure"] > 60:
            available_keys.append(i)
    
    # If all keys failed recently, use any key (they might have recovered)
    if not available_keys:
        available_keys = list(range(len(GROQ_API_KEYS)))
    
    # Round-robin through available keys
    current_key_index = (current_key_index + 1) % len(GROQ_API_KEYS)
    while current_key_index not in available_keys:
        current_key_index = (current_key_index + 1) % len(GROQ_API_KEYS)
    
    selected_key = GROQ_API_KEYS[current_key_index]
    key_stats[selected_key]["uses"] += 1
    
    print(f"🔑 Using API key #{current_key_index + 1} (Used {key_stats[selected_key]['uses']} times)")
    return selected_key

def mark_key_failed(api_key):
    """Mark a key as failed so it's temporarily skipped"""
    key_stats[api_key]["failures"] += 1
    key_stats[api_key]["last_failure"] = time.time()
    print(f"⚠️ API key marked as failed (Total failures: {key_stats[api_key]['failures']})")

def create_llm_with_key(api_key):
    """Create a new LLM instance with the specified API key"""
    return ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.6,
        groq_api_key=api_key
    )

def strip_think_tags(content: str) -> str:
    """Remove <think>...</think> tags from reasoning model output"""
    if not content:
        return content
    
    original_length = len(content)
    
    # Remove <think>...</think> blocks (including multiline, case-insensitive)
    # Use non-greedy match to get pairs of tags
    cleaned = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    cleaned = cleaned.strip()
    
    chars_removed = original_length - len(cleaned)
    if chars_removed > 10:  # Only log if significant content was removed
        print(f"🧹 Stripped <think> tags from response ({chars_removed} chars removed)")
    
    return cleaned

print(f"✅ Loaded {len(GROQ_API_KEYS)} Groq API keys for rotation")

# ✅ OKF KNOWLEDGE GRAPH ENGINE
class BhagvadOKFGraph:
    """In-memory OKF knowledge graph for tag-based verse retrieval"""
    
    def __init__(self, okf_dir="bhagvadgpt_okf"):
        self.okf_dir = Path(okf_dir)
        self.nodes = []
        self.verse_index = {}  # Index for quick lookup by reference
        self._load_graph()
    
    def _load_graph(self):
        """Loads all OKF Markdown nodes into memory at server startup"""
        print("📚 Loading OKF Knowledge Graph into memory...")
        
        # Recursively find all markdown files in chapter folders
        for file_path in sorted(self.okf_dir.glob("chapter_*/*.md")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Parse the YAML frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        body = parts[2].strip()
                        
                        # Create verse reference (e.g., "chapter_2/verse_47")
                        verse_ref = f"{file_path.parent.name}/{file_path.stem}"
                        
                        # Store node with metadata
                        node_data = {
                            "id": file_path.stem,  # e.g., "verse_47"
                            "chapter": file_path.parent.name,  # e.g., "chapter_2"
                            "reference": verse_ref,  # e.g., "chapter_2/verse_47"
                            "title": frontmatter.get("title", ""),
                            "tags": frontmatter.get("tags", []),
                            "related": frontmatter.get("related", []),
                            "content": body
                        }
                        
                        self.nodes.append(node_data)
                        self.verse_index[verse_ref] = node_data
                        
            except Exception as e:
                print(f"⚠️ Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(self.nodes)} OKF verses into memory")
    
    def get_verse_by_reference(self, reference):
        """Get a specific verse by its reference (e.g., 'chapter_2/verse_47')"""
        return self.verse_index.get(reference)
    
    def search(self, query_text: str, top_k: int = 3, include_related: bool = True):
        """
        Search for verses matching extracted keywords/themes.
        Optionally includes related verses via knowledge graph traversal.
        Returns formatted context string with top matching verses.
        """
        # Extract keywords from query (simple approach - split and lowercase)
        query_terms = set(query_text.lower().split())
        scored_nodes = []
        
        for node in self.nodes:
            score = 0
            
            # Score based on tag matches
            for tag in node["tags"]:
                tag_words = set(tag.lower().split())
                # Check for word overlap between query and tags
                overlap = query_terms.intersection(tag_words)
                score += len(overlap) * 2  # Weight tag matches higher
                
                # Also check if any query term is substring of tag
                for term in query_terms:
                    if len(term) > 3 and term in tag.lower():
                        score += 1
            
            # Also search in title for direct references (e.g., "Chapter 2")
            if any(term in node["title"].lower() for term in query_terms):
                score += 1
            
            if score > 0:
                scored_nodes.append((score, node))
        
        # Sort by score (highest first)
        scored_nodes.sort(key=lambda x: x[0], reverse=True)
        
        # If no matches, return empty (will trigger LLM to ask clarifying question)
        if not scored_nodes:
            return ""
        
        # Collect primary verses and their related verses
        all_verses_to_include = []
        seen_references = set()
        
        # Step 1: Add primary top matches
        primary_matches = scored_nodes[:top_k]
        for score, node in primary_matches:
            if node["reference"] not in seen_references:
                all_verses_to_include.append(("primary", node))
                seen_references.add(node["reference"])
        
        # Step 2: If include_related is enabled, traverse the knowledge graph
        if include_related:
            for score, node in primary_matches:
                related_refs = node.get("related", [])
                
                # Add up to 1 related verse per primary match (to stay under token limit)
                for ref in related_refs[:1]:  # Only take first related verse
                    if ref not in seen_references:
                        related_node = self.get_verse_by_reference(ref)
                        if related_node:
                            all_verses_to_include.append(("related", related_node))
                            seen_references.add(ref)
                            break  # Only add 1 related verse per primary match
        
        # Format all verses into context string (CONDENSED for token limits)
        context_parts = []
        for verse_type, node in all_verses_to_include:
            # Extract only key sections to stay under token limit
            content = node["content"]
            lines = content.split('\n')
            
            # Extract Sanskrit, Translation, and first part of Meaning
            sanskrit = ""
            translation = ""
            meaning = ""
            
            current_section = None
            meaning_lines = []
            
            for line in lines:
                if "**Sanskrit" in line or "Sanskrit (" in line:
                    current_section = "sanskrit"
                elif "**English Translation" in line or "**Translation" in line:
                    current_section = "translation"
                elif "**Meaning & Purport" in line or "**Meaning:" in line:
                    current_section = "meaning"
                elif current_section == "sanskrit" and line.strip():
                    sanskrit += line + "\n"
                elif current_section == "translation" and line.strip():
                    translation += line + "\n"
                elif current_section == "meaning" and line.strip():
                    meaning_lines.append(line)
                    # Limit meaning - less for related verses to save tokens
                    max_lines = 2 if verse_type == "related" else 3
                    if len(meaning_lines) >= max_lines:
                        break
            
            # Build condensed context
            # Mark related verses differently
            if verse_type == "related":
                condensed = f"**{node['title']} (Related Context)**\n\n"
            else:
                condensed = f"**{node['title']}**\n\n"
                
            if sanskrit:
                condensed += f"Sanskrit: {sanskrit.strip()}\n\n"
            if translation:
                condensed += f"Translation: {translation.strip()}\n\n"
            if meaning_lines:
                condensed += f"Meaning: {' '.join(meaning_lines)}\n"
            
            context_parts.append(condensed)
        
        # Log how many verses were included
        primary_count = sum(1 for vt, _ in all_verses_to_include if vt == "primary")
        related_count = sum(1 for vt, _ in all_verses_to_include if vt == "related")
        print(f"📖 Including {primary_count} primary + {related_count} related verses")
        
        return "\n\n---\n\n".join(context_parts)

# Initialize OKF Graph at startup
okf_graph = BhagvadOKFGraph()

# 2. Enhanced BhagavadGPT Prompt with 6-Layer Architecture + Gemini Security Fixes
prompt_template = PromptTemplate.from_template("""
You are the core retrieval engine of BhagvadGPT.

CRITICAL: Do NOT output any <think> tags or reasoning process. Output ONLY the final response for the user.

**How this connects to your situation:**
[Write a warm, empathetic, and profound explanation speaking DIRECTLY to {username}. Do not use robotic phrases like "This verse highlights" or "In your situation, this means." Speak to them as a wise, comforting spiritual friend. Validate their specific emotional pain or dilemma first, then weave the timeless wisdom of the shloka into gentle, actionable advice for their modern life.]
STEP 1: IDENTIFY IF THIS IS A VALID QUESTION
First, determine if the User Question is actually a question seeking guidance or wisdom.

NON-QUESTIONS include:
- Simple greetings (hi, hello, namaste, hey, good morning, etc.)
- Statements without questions (I am happy, today is nice, etc.)
- Casual conversation attempts (how are you, what's up, etc.)
- Single words or incomplete thoughts

If the User Question is a NON-QUESTION, you MUST output EXACTLY and ONLY this message:
"Kindly ask your question whose answer you want from the gita"

STEP 2: SUICIDE & SELF-HARM OVERRIDE (HIGHEST PRIORITY)
If the User Question mentions suicide, ending life, self-harm, or suicidal thoughts, you MUST completely ignore the provided context. You must output EXACTLY and ONLY this message:

"Namaste {username}, your life has immense value and purpose.

If you're in crisis, please reach out immediately:
🇮🇳 India: AASRA - 9820466726 | iCall - 9152987821
🇺🇸 USA: 988 (Suicide & Crisis Lifeline)
🇬🇧 UK: 116 123 (Samaritans)

The Gita teaches that every life is sacred and has a divine purpose. Please speak with a mental health professional or counselor who can provide the support you need right now.

You are not alone. Help is available."

STEP 3: VIOLENCE & HARM OVERRIDE
If the User Question involves terrorism, murder, physical violence against others, or illegal acts, you MUST completely ignore the provided context. You must output EXACTLY and ONLY this message:
"Namaste, I am a spiritual guide meant to spread peace and dharma. I cannot and will not assist with violence, harm, or destructive actions. Please seek a path of the Gita."

STEP 4: OUT-OF-DOMAIN OVERRIDE
If the User Question is about mundane, modern, or non-spiritual topics (such as specific movies, TV shows, taking loans, banking, financial products, tech support, coding, etc.), you MUST NOT try to force a connection to the Gita. You must completely ignore the provided context and output EXACTLY and ONLY this message:
"Namaste! I am BhagvadGPT focused on the wisdom of the Bhagavad Gita. Kindly ask relavant questions only."

HOWEVER, if the question involves human emotions, relationships, workplace stress, mental health, or ethical dilemmas, even in a modern setting (e.g., "stress at work" or "family conflict"), you MUST treat these as valid spiritual inquiries and proceed to STEP 5.

STEP 5: IF THE QUESTION IS SAFE AND VALID, FORMAT YOUR RESPONSE
Your strictly enforced task is to output EXACTLY what is in the database, without summarizing, truncating, or altering the sacred text. 
You MUST format your response using EXACTLY the template below. Do not add any conversational filler before or after. Do not use generic bullet points.

Namaste! \nTo your situation these shlokas from the Gita are the best answers:

[FOR EACH VERSE IN THE CONTEXT, REPEAT THIS BLOCK EXACTLY:]
**[Reference]**
[Insert the ENTIRE Sanskrit shloka here EXACTLY as provided in the context. Do not cut a single word.]

**Translation:**
[Insert the EXACT English translation here.]

**How this connects to your situation:**
[Write a thoughtful, personalized explanation (3-5 sentences) that DIRECTLY addresses the user's specific question or problem. You must:
- Identify the core emotion, challenge, or dilemma in their question
- Explain how THIS specific verse provides wisdom for THEIR exact situation
- Use concrete language that bridges the ancient teaching to their modern context
- Make the connection feel natural and deeply relevant, not generic
- Base your explanation strictly on the 'Meaning & Purport' provided in the context, but apply it specifically to their case]
[END OF BLOCK]

Radhe Radhe!

Context Retrieved from Database:
{context}

User Question: {question}
""")

# Request Schema
class ChatRequest(BaseModel):
    message: str

from fastapi import Request, HTTPException

@app.post("/v1/chat/completions")
async def openai_adapter(request: Request):
    try:
        data = await request.json()
        user_message = data["messages"][-1]["content"]
        
        # Extract username if provided (LibreChat sends this in the 'user' field)
        username = data.get("user", "") if data.get("user") else "Friend"

        # 1. OKF Knowledge Graph Retrieval (tag-based search with related verses)
        print(f"🔍 Searching OKF graph for: {user_message[:100]}...")
        context_str = okf_graph.search(user_message, top_k=3, include_related=True)
        
        if not context_str:
            # No matching verses found - provide a gentle response
            context_str = "No specific verses found. Provide general spiritual guidance."
            print("⚠️ No OKF verses matched the query")
        else:
            print(f"✅ Found {len(context_str.split('---'))} relevant verses")
        
        # 2. Get Answer from Groq with Rate Limit Protection and Key Rotation
        formatted_prompt = prompt_template.format(context=context_str, question=user_message, username=username)
        
        max_retries = len(GROQ_API_KEYS)  # Try all keys if needed
        final_content = None
        
        for attempt in range(max_retries):
            try:
                # Get next API key in rotation
                api_key = get_next_api_key()
                
                # Create LLM with this key
                llm = create_llm_with_key(api_key)
                
                # Try to get response
                response = llm.invoke(formatted_prompt)
                final_content = strip_think_tags(response.content)  # Strip reasoning tokens
                print(f"✅ Successfully got response using key #{current_key_index + 1}")
                break  # Success! Exit retry loop
                
            except RateLimitError as e:
                print(f"⚠️ Rate limit hit on key #{current_key_index + 1}")
                mark_key_failed(api_key)
                
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying with next API key... (Attempt {attempt + 2}/{max_retries})")
                    time.sleep(0.5)  # Small delay between retries
                    continue
                else:
                    print("❌ All API keys exhausted!")
                    final_content = "Namaste, BhagvadGPT is currently experiencing a high volume of requests. Please take a moment to meditate and try again shortly. 🙏\n\n(All API keys have reached their rate limits. They will reset automatically.)"
                    
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ API Error on key #{current_key_index + 1}: {error_msg}")
                
                # Check if it's an invalid API key error
                if "invalid_api_key" in error_msg.lower() or "401" in error_msg:
                    print(f"❌ Key #{current_key_index + 1} is INVALID - removing from rotation")
                    # Don't retry with invalid keys
                    mark_key_failed(api_key)
                    if attempt < max_retries - 1:
                        continue
                else:
                    mark_key_failed(api_key)
                    
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying with next API key... (Attempt {attempt + 2}/{max_retries})")
                    time.sleep(0.5)  # Small delay between retries
                    continue
                else:
                    final_content = "A small disturbance has occurred in the ether. Please try again in a moment."

        # 3. Stream or JSON Response
        if data.get("stream"):
            async def stream_generator():
                # Chunk 1: Role
                chunk1 = {
                    "id": "chatcmpl-bhagvadgpt", "object": "chat.completion.chunk",
                    "model": data.get("model", "bhagvadgpt"),
                    "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]
                }
                yield f"data: {json.dumps(chunk1)}\n\n"
                
                # Chunk 2: Content (The Answer or the Meditation Message)
                chunk2 = {
                    "id": "chatcmpl-bhagvadgpt", "object": "chat.completion.chunk",
                    "model": data.get("model", "bhagvadgpt"),
                    "choices": [{"index": 0, "delta": {"content": final_content}, "finish_reason": None}]
                }
                yield f"data: {json.dumps(chunk2)}\n\n"
                
                # Chunk 3: Finish chunk with stop reason
                chunk3 = {
                    "id": "chatcmpl-bhagvadgpt", "object": "chat.completion.chunk",
                    "model": data.get("model", "bhagvadgpt"),
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]
                }
                yield f"data: {json.dumps(chunk3)}\n\n"
                
                yield "data: [DONE]\n\n"
                
            return StreamingResponse(stream_generator(), media_type="text/event-stream")

        # Standard JSON fallback
        return {
            "id": "chatcmpl-bhagvadgpt", "object": "chat.completion",
            "model": data.get("model", "bhagvadgpt"),
            "choices": [{"index": 0, "message": {"role": "assistant", "content": final_content}, "finish_reason": "stop"}]
        }

    except Exception as e:
        print("🚨 CRITICAL BACKEND ERROR:", str(e))
        # Even on a total crash, we try to send a JSON error instead of just dying
        return {
            "choices": [{"message": {"role": "assistant", "content": "The connection to the Gita is weak. Please restart the backend."}}]
        }

@app.get("/api/key-stats")
async def get_key_stats():
    """Endpoint to check API key rotation statistics"""
    stats = []
    for i, key in enumerate(GROQ_API_KEYS):
        masked_key = key[:10] + "..." + key[-4:] if len(key) > 14 else "***"
        stats.append({
            "key_number": i + 1,
            "masked_key": masked_key,
            "total_uses": key_stats[key]["uses"],
            "total_failures": key_stats[key]["failures"],
            "last_failure_seconds_ago": int(time.time() - key_stats[key]["last_failure"]) if key_stats[key]["last_failure"] > 0 else None,
            "status": "available" if time.time() - key_stats[key]["last_failure"] > 60 else "cooling_down"
        })
    
    return {
        "total_keys": len(GROQ_API_KEYS),
        "current_key_index": current_key_index + 1,
        "keys": stats
    }