with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
skip_next = 0
i = 0
removed = 0

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Skip meaning section detection
    if '**Meaning & Purport' in stripped or '**Meaning:' in stripped:
        # Remove the elif line that sets current_section = "meaning"
        if 'current_section = "meaning"' in stripped:
            i += 1
            removed += 1
            continue
    
    # Skip meaning accumulation block
    if 'current_section == "meaning" and line.strip():' in stripped:
        # Skip this line and next 4 lines (append, comment, max_lines, if break)
        i += 5
        removed += 5
        continue
    
    # Skip meaning output line
    if stripped.startswith('if meaning_lines:') and i + 1 < len(lines):
        next_stripped = lines[i+1].strip()
        if 'Meaning:' in next_stripped and 'condensed +=' in next_stripped:
            i += 2
            removed += 2
            continue
    
    output.append(line)
    i += 1

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Removed {removed} lines related to meaning context")
