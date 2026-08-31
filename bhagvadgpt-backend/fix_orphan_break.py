with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove orphaned "meaning" detection and orphaned "break" lines left by previous script
import re

# Remove the elif that detects meaning section header (now useless since we don't collect meaning)
content = re.sub(
    r'\s+elif "\*\*Meaning & Purport" in line or "\*\*Meaning:" in line:\s+current_section = "meaning"\n',
    '\n',
    content
)

# Remove orphaned break lines that were part of the meaning block
# Pattern: a line that is just whitespace + "break" after a translation line
content = re.sub(
    r'(                elif current_section == "translation" and line\.strip\(\):\s+translation \+= line \+ "\\n"\n)(\s+break\n)',
    r'\1',
    content
)

# Also remove meaning_lines variable declarations (no longer needed)
content = re.sub(r'\s+meaning_lines = \[\]\n', '\n', content)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")
