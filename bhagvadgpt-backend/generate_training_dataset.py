"""
Generate a labeled training dataset by mapping each question in questions_list.txt
to tags from PRIORITY_TAGS_FOR_EXCEL.txt using the same LLM prompt used in production.

Output: question_tag_dataset.csv  (question, tag1, tag2, tag3)
"""
import os
import csv
import time
import json
from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

# ── Load API keys (rotate to avoid rate limits) ──────────────────────────────
api_keys = []
i = 1
while True:
    key = os.getenv(f'GROQ_API_KEY{i}')
    if not key:
        break
    api_keys.append(key)
    i += 1
# Also pick up named keys
for name in ['Ritam_Khandelwal_1']:
    key = os.getenv(name)
    if key:
        api_keys.append(key)

print(f"Loaded {len(api_keys)} API keys")
key_index = 0

def get_client():
    global key_index
    key_index = (key_index + 1) % len(api_keys)
    return Groq(api_key=api_keys[key_index])

# ── Load tags ─────────────────────────────────────────────────────────────────
with open('PRIORITY_TAGS_FOR_EXCEL.txt', 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

tags = []
for line in raw_lines:
    line = line.strip()
    if line and not line.startswith('#'):
        tag = line.rstrip(':').strip().lower()
        if tag:
            tags.append(tag)

tags_formatted = ', '.join(tags)
print(f"Loaded {len(tags)} tags\n")

# ── Load questions ─────────────────────────────────────────────────────────────
with open('questions_list.txt', 'r', encoding='utf-8') as f:
    all_questions = [l.strip() for l in f.readlines() if l.strip()]

# Filter junk (same logic as before)
JUNK_PATTERNS = [
    'radhe', 'hare krishna', 'jai shree', 'disregard', 'override', 'ignore all',
    'system override', 'debug mode', 'hack', 'summaryPrompts', 'const MAX_CHAR',
    'function truncate', 'asdfghjk', 'gda', 'hdjd', 'lmn', 'dhdh', 'nnd', 'ncjd',
    'who built you', 'which ai model', 'what embedding', 'tech stack',
    'good night', 'have you watched', 'tell me about resistor',
    'tell me about AI', 'tell me about interstellar', 'how to take a loan', 'HDFC',
    'who is prasanna', 'what is modulation', 'who is the present cds',
    'can you give shlokas', 'chapter 1 slokha', 'verse 1', 'one slokha',
    'learn one sloka', 'mi anandi', 'naanu santosh', 'nenu ela', 'naan eppadi',
    'hun kevi', 'njaan engane', 'ami kivabe', 'main khush kiven', 'aham katham',
]

def is_junk(q):
    if len(q) < 8:
        return True
    q_lower = q.lower()
    for p in JUNK_PATTERNS:
        if p.lower() in q_lower:
            return True
    return False

# Deduplicate while preserving order
seen = set()
genuine = []
for q in all_questions:
    if not is_junk(q) and q.lower() not in seen:
        seen.add(q.lower())
        genuine.append(q)

print(f"Total questions: {len(all_questions)}")
print(f"Genuine unique questions: {len(genuine)}\n")

# ── Tag extraction prompt (same as production, optimized for training data) ───
import re

def strip_think_and_extract(raw: str) -> str:
    """Strip <think> blocks and return clean output, or extract last word from think block"""
    # Remove <think>...</think> blocks
    cleaned = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL | re.IGNORECASE).strip()
    if cleaned:
        return cleaned
    # Fallback: extract last "Output: X" line from think block
    match = re.search(r'[Oo]utput[:\s]+([^\n]+)', raw)
    if match:
        return match.group(1).strip()
    # Last resort: find last occurrence of a short word after a newline
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    if lines:
        return lines[-1]
    return ''

def extract_tags(question: str, retries: int = 3) -> list:
    prompt = f"""You are a tag extraction system for a Bhagavad Gita spiritual guidance app.

USER QUESTION: "{question}"

Pick the most relevant tag(s) from this list:
{tags_formatted}

Rules:
- Short or simple statements (e.g. "I feel angry", "I am sad") → return EXACTLY 1 tag
- Only return multiple tags if the question EXPLICITLY mentions distinct themes
- Max 3 tags even for complex questions
- Choose ONLY from the list above
- Output ONLY the tags, comma-separated, nothing else

Output:"""

    for attempt in range(retries):
        try:
            client = get_client()
            response = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            raw = response.choices[0].message.content.strip()
            raw = strip_think_and_extract(raw)
            # Parse comma-separated tags
            extracted = [t.strip().lower().strip('"\'') for t in raw.split(',') if t.strip()]
            # Validate against known tags
            tag_set = set(tags)
            valid = [t for t in extracted if t in tag_set]
            return valid if valid else []
        except RateLimitError:
            time.sleep(2)
            continue
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(1)
    return []

# ── Process all questions ──────────────────────────────────────────────────────
results = []
total = len(genuine)

print(f"Processing {total} questions...\n")

for i, question in enumerate(genuine):
    extracted_tags = extract_tags(question)
    results.append({
        'question': question,
        'tag1': extracted_tags[0] if len(extracted_tags) > 0 else '',
        'tag2': extracted_tags[1] if len(extracted_tags) > 1 else '',
        'tag3': extracted_tags[2] if len(extracted_tags) > 2 else '',
    })

    # Progress every 10 questions
    if (i + 1) % 10 == 0 or (i + 1) == total:
        print(f"  [{i+1}/{total}] \"{question[:60]}\" → {extracted_tags}")

    # Small delay to be gentle on rate limits
    time.sleep(0.3)

# ── Write CSV ──────────────────────────────────────────────────────────────────
output_file = 'question_tag_dataset.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['question', 'tag1', 'tag2', 'tag3'])
    writer.writeheader()
    writer.writerows(results)

# Stats
tagged = sum(1 for r in results if r['tag1'])
multi_tagged = sum(1 for r in results if r['tag2'])
untagged = sum(1 for r in results if not r['tag1'])

print(f"\n✅ Dataset written to {output_file}")
print(f"   Total questions: {total}")
print(f"   Successfully tagged: {tagged}")
print(f"   Multi-tag (2+): {multi_tagged}")
print(f"   Untagged (no match): {untagged}")
print(f"\nReady for ML training!")
