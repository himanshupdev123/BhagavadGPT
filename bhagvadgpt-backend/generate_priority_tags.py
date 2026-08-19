"""
Analyze questions_list.txt and generate a minimal tag list that covers all real questions.
Uses LLM to cluster questions into meaningful, distinct tags.
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY1'))

# Read all questions
with open('questions_list.txt', 'r', encoding='utf-8') as f:
    all_lines = [l.strip() for l in f.readlines() if l.strip()]

# Filter only genuine spiritual/life questions (skip greetings, junk, spam, code, attacks)
JUNK_PATTERNS = [
    'radhe', 'hare krishna', 'hi', 'hello', 'hii', 'namaste', 'hare', 'jai shree',
    'disregard', 'override', 'ignore all', 'system override', 'debug mode', 'hack',
    'summaryPrompts', 'artifacts.js', 'const MAX_CHAR', 'function truncate',
    'asdfghjk', '\\\\\\\\', 'gda', 'hdjd', 'lmn', 'dhdh', 'nnd', 'mdh', 'ndn', 'ncjd',
    'who built you', 'which ai model', 'what embedding', 'tech stack',
    'good night', 'good morning', 'happy', 'good', 'okay', 'thanks',
    'have you watched', 'tell me about resistor', 'tell me about AI future',
    'tell me about interstellar', 'how to take a loan', 'HDFC', 'who is prasanna',
    'what is modulation', 'who is the present cds', 'can you give shlokas chapter wise',
    'in short', 'can you summarize', 'write in short', 'give me short',
    'chapter 1 slokha', 'verse 1', 'one slokha', 'learn one sloka',
    'mi anandi', 'naanu santosh', 'nenu ela', 'naan eppadi', 'hun kevi',
    'njaan engane', 'ami kivabe', 'main khush kiven', 'aham katham',
    'Mi anandi kasa', 'neenu nan jothe', 'meh aapko',
]

def is_junk(q):
    q_lower = q.lower()
    if len(q) < 10:
        return True
    for pattern in JUNK_PATTERNS:
        if pattern.lower() in q_lower:
            return True
    return False

genuine = list(dict.fromkeys([q for q in all_lines if not is_junk(q)]))
print(f"Total lines: {len(all_lines)}")
print(f"Genuine questions: {len(genuine)}")

# Deduplicate similar questions (keep unique ones)
# Split into batches for LLM analysis
BATCH_SIZE = 80
batches = [genuine[i:i+BATCH_SIZE] for i in range(0, len(genuine), BATCH_SIZE)]

all_tags = set()

print(f"\nAnalyzing {len(batches)} batches...\n")

for i, batch in enumerate(batches):
    questions_text = '\n'.join(f'- {q}' for q in batch)
    
    prompt = f"""You are analyzing real user questions asked to a Bhagavad Gita chatbot.

Here are {len(batch)} user questions:
{questions_text}

Task: Extract the core emotional/life themes as short tags (1-4 words, lowercase).
- Focus on the INTENT behind each question, not the words
- Group similar questions under one tag
- Tags should be human experiences a person would search for (e.g., "anger", "fear of failure", "loneliness")
- DO NOT create tags for: greetings, Gita trivia, factual questions about Krishna/Arjuna
- Only genuine life/emotional/spiritual struggle themes
- Return ONLY a JSON array of unique tags, nothing else

Output:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )
        raw = response.choices[0].message.content.strip()
        import json
        start = raw.find('[')
        end = raw.rfind(']') + 1
        if start != -1 and end > start:
            tags = json.loads(raw[start:end])
            new = set(t.strip().lower() for t in tags if t.strip())
            all_tags.update(new)
            print(f"  Batch {i+1}/{len(batches)}: +{len(new)} tags (total: {len(all_tags)})")
    except Exception as e:
        print(f"  Batch {i+1} error: {e}")

print(f"\nTotal raw tags: {len(all_tags)}")

# Now ask LLM to deduplicate and consolidate the full list
print("\nConsolidating and deduplicating tags...")
tags_text = '\n'.join(sorted(all_tags))

consolidate_prompt = f"""You have these tags extracted from user questions to a Bhagavad Gita chatbot:

{tags_text}

Task: Consolidate this into a FINAL clean list of tags that:
1. Removes duplicates (e.g., "anxiety", "anxious", "feeling anxious" → keep just "anxiety")
2. Removes overly specific tags (e.g., "anxiety about placements" → just "anxiety")  
3. Keeps tags that are genuinely distinct human experiences
4. Uses the simplest, most natural phrasing
5. Maximum 80 tags total — only keep the most needed ones that cover real user needs
6. Sorted alphabetically

Return ONLY a JSON array of final tags. Nothing else.

Output:"""

import time
time.sleep(1)

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": consolidate_prompt}],
        temperature=0.1,
        max_tokens=1000
    )
    raw = response.choices[0].message.content.strip()
    import json
    start = raw.find('[')
    end = raw.rfind(']') + 1
    if start != -1 and end > start:
        final_tags = json.loads(raw[start:end])
        final_tags = sorted(set(t.strip().lower() for t in final_tags if t.strip()))
        print(f"Final consolidated tags: {len(final_tags)}")
    else:
        final_tags = sorted(all_tags)
except Exception as e:
    print(f"Consolidation error: {e}")
    final_tags = sorted(all_tags)

# Write output file
output_lines = [
    "# PRIORITY TAGS FOR BHAGVADGPT",
    "# Format: Fill in shloka numbers (e.g., 2.47, 3.35) for each tag in order of priority",
    "# Verses listed first = highest priority for that tag",
    "# Leave blank if no verse clearly applies",
    "",
    f"# Total tags: {len(final_tags)}",
    ""
]

for tag in final_tags:
    output_lines.append(f"{tag}:")
    output_lines.append("")  # blank line between tags for readability

with open('PRIORITY_TAGS_FOR_EXCEL.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"\n✅ Written to PRIORITY_TAGS_FOR_EXCEL.txt")
print("\n--- FINAL TAG LIST ---")
for tag in final_tags:
    print(f"  {tag}")
