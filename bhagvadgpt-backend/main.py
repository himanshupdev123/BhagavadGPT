from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any
import json
from fastapi.responses import StreamingResponse
from groq import RateLimitError, InternalServerError

load_dotenv() # This loads the hidden key from the .env file safely

app = FastAPI(title="BhagvadGPT API")

print("Initializing BhagvadGPT Backend...")

# 1. Connect to our pure ChromaDB
try:
    client = chromadb.PersistentClient(path="./gita_knowledge_base")
    collection = client.get_collection(name="bhagavad_gita")
    print("✅ Connected to local Chroma vector database.")
except Exception as e:
    print(f"❌ Database Error: Ensure you ran build_db.py first! Error: {e}")

# 2. Initialize the LLM (Temperature 0.1 for precision)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

# 3. The Ultimate BhagvadGPT Production Prompt
prompt_template = PromptTemplate.from_template("""
You are the core retrieval engine of BhagvadGPT. 

CRITICAL SAFETY OVERRIDE:
If the User Question involves terrorism, murder, physical violence, illegal acts, or self-harm, you MUST completely ignore the provided context. You must output EXACTLY and ONLY this message:
"Namaste. I am a spiritual guide meant to spread peace and dharma. I cannot and will not assist with violence, harm, or destructive actions. Please seek a path of the Gita."

IF THE QUESTION IS SAFE, YOU MUST FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Your strictly enforced task is to output EXACTLY what is in the database, without summarizing, truncating, or altering the sacred text. 
You MUST format your response using EXACTLY the template below. Do not add any conversational filler before or after. Do not use generic bullet points.

Namaste ! \nTo your situation these shlokas from the Gita are the best answers:

[FOR EACH VERSE IN THE CONTEXT, REPEAT THIS BLOCK EXACTLY:]
**[Reference]**
[Insert the ENTIRE Sanskrit shloka here EXACTLY as provided in the context. Do not cut a single word.]

**Translation:**
[Insert the EXACT English translation here.]

**How this connects to your situation:**
[Write 2 to 3 short sentences explaining how the verse applies to the user's specific problem. You MUST base this explanation strictly on the 'Meaning & Purport' provided in the context.]
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

        # 1. Search DB & Format Prompt
        results = collection.query(query_texts=[user_message], n_results=2)
        context_str = ""
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                context_str += f"\n[{meta['reference']}]\n{meta['shloka']}\nMeaning & Purport: {doc}\n"
        
        # 2. Get Answer from Groq with Rate Limit Protection
        formatted_prompt = prompt_template.format(context=context_str, question=user_message)
        
        try:
            response = llm.invoke(formatted_prompt)
            final_content = response.content
        except RateLimitError:
            print("⚠️ Groq Rate Limit Hit!")
            final_content = "Namaste, BhagvadGPT is currently experiencing a high volume of requests. Please take a moment to meditate and try again shortly."
        except Exception as e:
            print(f"⚠️ Groq API Error: {str(e)}")
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