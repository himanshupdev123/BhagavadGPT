"""
Enrich tags for chapter 1-6 verses that already have tags.
Uses Groq LLM to suggest additional relevant tags based on existing tags + verse meaning.
Skips verses with empty tags entirely.
Also updates the master tag list.
"""
import os
import time
import yaml
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Use first available key
api_key = os.getenv('GROQ_API_KEY1')
client = Groq(api_key=api_key)

KNOWLEDGE_BASE = Path("bhagvadgpt_okf")
MASTER_TAGS_FILE = Path("100_MASTER_TAGS.txt")

# Load master tags
master_tags = set(t.strip().lower() for t in MASTER_TAGS_FILE.read_text(encoding='utf-8').splitlines() if t.strip())
print(f"Loaded {len(master_tags)} master tags\n")

def enrich_tags_for_verse(verse_ref: str, existing_tags: list, title: str, translation: str, purport: str) -> list:
    """Ask Groq to enrich the tags for a verse"""
    
    prompt = f"""You are helping tag Bhagavad Gita verses for a spiritual chatbot that matches user questions to relevant verses.

Verse: {title}

English Translation:
{translation}

Meaning/Purport:
{purport}

Current tags assigned: {', '.join(existing_tags)}

Task: Based on the verse's meaning and the existing tags, suggest ADDITIONAL tags that are missing but clearly relevant. 
- Focus on modern human experiences: emotions, life situations, struggles, mental states
- Tags should be short (1-4 words), lowercase, practical
- Only add tags that are genuinely needed and strongly relevant to this verse
- Do NOT repeat existing tags
- Return ONLY a JSON array of new tags to add, nothing else
- Maximum 8 new tags

Example output: ["overthinking", "fear of failure", "mental peace", "purpose"]

Output:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        raw = response.choices[0].message.content.strip()
        # Extract JSON array
        start = raw.find('[')
        end = raw.rfind(']') + 1
        if start != -1 and end > start:
            new_tags = json.loads(raw[start:end])
            return [t.strip().lower() for t in new_tags if t.strip()]
        return []
    except Exception as e:
        print(f"  ⚠️ LLM error: {e}")
        return []


# Collect all tagged verses from chapters 1-6
tagged_verses = []
for ch in range(1, 7):
    ch_dir = KNOWLEDGE_BASE / f"chapter_{ch}"
    if not ch_dir.exists():
        continue
    for verse_file in sorted(ch_dir.glob("verse_*.md")):
        content = verse_file.read_text(encoding='utf-8')
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
        fm = yaml.safe_load(parts[1])
        tags = fm.get('tags', [])
        if not tags:  # Skip untagged verses
            continue
        
        body = parts[2]
        # Extract translation and purport from body
        trans_start = body.find('**English Translation:**')
        purport_start = body.find('**Meaning & Purport:**')
        modern_start = body.find('**Modern Applications:**')
        
        translation = ""
        purport = ""
        
        if trans_start != -1 and purport_start != -1:
            translation = body[trans_start + len('**English Translation:**'):purport_start].strip()
        
        if purport_start != -1:
            purport_end = modern_start if modern_start != -1 else len(body)
            purport = body[purport_start + len('**Meaning & Purport:**'):purport_end].strip()
        
        tagged_verses.append({
            'path': verse_file,
            'fm': fm,
            'body': body,
            'tags': tags,
            'translation': translation,
            'purport': purport,
            'title': fm.get('title', '')
        })

print(f"Found {len(tagged_verses)} tagged verses in chapters 1-6\n")
print("=" * 60)

all_new_tags = set()
updated_count = 0

for i, verse in enumerate(tagged_verses):
    ref = verse['path'].parent.name + '/' + verse['path'].stem
    print(f"[{i+1}/{len(tagged_verses)}] {ref}")
    print(f"  Existing tags: {verse['tags']}")
    
    new_tags = enrich_tags_for_verse(
        ref,
        verse['tags'],
        verse['title'],
        verse['translation'],
        verse['purport']
    )
    
    if new_tags:
        # Merge, keeping existing tags first
        existing_set = set(t.lower() for t in verse['tags'])
        truly_new = [t for t in new_tags if t.lower() not in existing_set]
        
        if truly_new:
            print(f"  + Adding: {truly_new}")
            merged_tags = verse['tags'] + truly_new
            
            # Update frontmatter
            verse['fm']['tags'] = merged_tags
            verse['fm']['updated'] = '2026-08-14'
            
            # Write back to file
            new_fm = yaml.dump(verse['fm'], default_flow_style=False, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{new_fm}---{verse['body']}"
            verse['path'].write_text(new_content, encoding='utf-8')
            
            all_new_tags.update(t.lower() for t in truly_new)
            updated_count += 1
        else:
            print(f"  (no new tags needed)")
    else:
        print(f"  (no new tags suggested)")
    
    # Rate limiting - be gentle with the API
    time.sleep(0.5)

print("\n" + "=" * 60)
print(f"✅ Updated {updated_count} verse files")
print(f"   New unique tags discovered: {len(all_new_tags)}")

# Update master tags list
new_master_tags = all_new_tags - master_tags
if new_master_tags:
    print(f"\n📋 New tags to add to master list ({len(new_master_tags)}):")
    for t in sorted(new_master_tags):
        print(f"   + {t}")
    
    # Append new tags to master list
    current_content = MASTER_TAGS_FILE.read_text(encoding='utf-8').rstrip()
    new_content = current_content + '\n' + '\n'.join(sorted(new_master_tags)) + '\n'
    MASTER_TAGS_FILE.write_text(new_content, encoding='utf-8')
    print(f"\n✅ Master tags list updated: {len(master_tags)} → {len(master_tags) + len(new_master_tags)} tags")
else:
    print("\n✅ No new tags to add to master list (all already present)")

print("\nDone!")
