"""Remove the Meaning section from all three context formatting functions"""
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove meaning extraction and inclusion from all 3 format functions
# Pattern 1: the meaning_lines accumulation block
old1 = '''            elif current_section == "meaning" and line.strip():
                meaning_lines.append(line)
                    # Limit meaning - less for related verses to save tokens
                max_lines = 3 if verse_type == "related" else 5
                if len(meaning_lines) >= max_lines:
                    break'''

# There are slight variations — let's just replace the meaning output lines
# Remove "if meaning_lines: condensed += ..." lines
import re

# Remove meaning accumulation blocks (all 3 occurrences)
content = re.sub(
    r'            elif current_section == "meaning" and line\.strip\(\):\s+'
    r'meaning_lines\.append\(line\)\s+'
    r'.*?max_lines = \d+ if verse_type.*?\n\s+if len\(meaning_lines\) >= max_lines:\s+break\n',
    '',
    content,
    flags=re.DOTALL
)

# Remove meaning output lines
content = re.sub(
    r'\s+if meaning_lines:\s+condensed \+= f"Meaning: \{.*?\}\\n"\n',
    '\n',
    content
)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - meaning sections removed")
