"""
Generate a tag → shlokas mapping dataset from the knowledge base.
For each tag in PRIORITY_TAGS_FOR_EXCEL.txt, find all verses that have that tag
in their frontmatter. Output: tag_shloka_dataset.csv (tag, shloka_ref, title, translation)
"""
import csv
import yaml
from pathlib import Path

# Load priority tags
with open('PRIORITY_TAGS_FOR_EXCEL.txt', 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

priority_tags = []
for line in raw_lines:
    line = line.strip()
    if line and not line.startswith('#'):
        tag = line.rstrip(':').strip().lower()
        if tag:
            priority_tags.append(tag)

priority_tag_set = set(priority_tags)
print(f"Loaded {len(priority_tags)} priority tags")

# Scan all verse files
kb = Path('bhagvadgpt_okf')
rows = []
tag_coverage = {tag: [] for tag in priority_tags}

for verse_file in sorted(kb.glob('chapter_*/*.md')):
    content = verse_file.read_text(encoding='utf-8')
    if not content.startswith('---'):
        continue

    parts = content.split('---', 2)
    if len(parts) < 3:
        continue

    fm = yaml.safe_load(parts[1])
    body = parts[2]

    verse_tags = [t.lower().strip() for t in fm.get('tags', []) if t]
    shloka_ref = f"{fm.get('chapter', '?')}.{fm.get('verse_number', '?')}"
    title = fm.get('title', '')

    # Extract translation
    translation = ''
    in_translation = False
    for line in body.split('\n'):
        if '**English Translation' in line or '**Translation' in line:
            in_translation = True
            continue
        if in_translation:
            if line.strip().startswith('**') and line.strip() != '**':
                break
            if line.strip():
                translation += line.strip() + ' '
                if len(translation) > 200:
                    break

    translation = translation.strip()

    # Match verse tags against priority tags
    for vtag in verse_tags:
        if vtag in priority_tag_set:
            rows.append({
                'tag': vtag,
                'shloka_ref': shloka_ref,
                'title': title,
                'translation': translation[:200]
            })
            tag_coverage[vtag].append(shloka_ref)

# Sort by tag then shloka ref
rows.sort(key=lambda r: (r['tag'], r['shloka_ref']))

# Write CSV
output_file = 'tag_shloka_dataset.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['tag', 'shloka_ref', 'title', 'translation'])
    writer.writeheader()
    writer.writerows(rows)

# Stats
covered_tags = [t for t in priority_tags if tag_coverage[t]]
uncovered_tags = [t for t in priority_tags if not tag_coverage[t]]

print(f"\n✅ Written to {output_file}")
print(f"   Total rows: {len(rows)}")
print(f"   Tags with at least 1 shloka: {len(covered_tags)}/{len(priority_tags)}")
print(f"   Tags with no shloka yet: {len(uncovered_tags)}")
if uncovered_tags:
    print(f"\n   Uncovered tags (fill these in your PriorityIndex sheet):")
    for t in uncovered_tags:
        print(f"     - {t}")

print(f"\n   Top 10 most covered tags:")
top = sorted(covered_tags, key=lambda t: len(tag_coverage[t]), reverse=True)[:10]
for t in top:
    print(f"     {t}: {len(tag_coverage[t])} shlokas")
