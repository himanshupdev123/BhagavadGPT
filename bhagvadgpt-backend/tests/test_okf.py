import yaml
from pathlib import Path

# Test OKF loading
okf_dir = Path("bhagvadgpt_okf")
nodes = []

print("Starting OKF load test...")
for file_path in sorted(okf_dir.glob("chapter_*/*.md")):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
                
                nodes.append({
                    "id": file_path.stem,
                    "chapter": file_path.parent.name,
                    "title": frontmatter.get("title", ""),
                    "tags": frontmatter.get("tags", []),
                    "content": body[:100]  # Just first 100 chars for test
                })
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

print(f"✅ Loaded {len(nodes)} verses")
print(f"Sample verse: {nodes[100]['title']}")
print(f"Sample tags: {nodes[100]['tags']}")
