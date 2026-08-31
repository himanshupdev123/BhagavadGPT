with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'max_lines = 2 if verse_type == "related" else 3'
new = 'max_lines = 3 if verse_type == "related" else 5'
count = content.count(old)
content = content.replace(old, new)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Replaced {count} occurrences")
