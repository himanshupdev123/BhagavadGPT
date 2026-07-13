print("Testing imports...")
from dotenv import load_dotenv
import os

print("Loading environment...")
load_dotenv()

print("Testing API keys...")
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY1"),
    os.getenv("GROQ_API_KEY2"), 
    os.getenv("GROQ_API_KEY3"),
    os.getenv("GROQ_API_KEY4"),
    os.getenv("GROQ_API_KEY5"), 
]
GROQ_API_KEYS = [key for key in GROQ_API_KEYS if key]
print(f"Found {len(GROQ_API_KEYS)} API keys")

print("Importing OKF Graph...")
import yaml
from pathlib import Path

class BhagvadOKFGraph:
    def __init__(self, okf_dir="bhagvadgpt_okf"):
        self.okf_dir = Path(okf_dir)
        self.nodes = []
        self._load_graph()
    
    def _load_graph(self):
        print("📚 Loading OKF Knowledge Graph...")
        for file_path in sorted(self.okf_dir.glob("chapter_*/*.md")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        body = parts[2].strip()
                        
                        self.nodes.append({
                            "id": file_path.stem,
                            "chapter": file_path.parent.name,
                            "title": frontmatter.get("title", ""),
                            "tags": frontmatter.get("tags", []),
                            "content": body
                        })
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"✅ Loaded {len(self.nodes)} verses")
    
    def search(self, query_text, top_k=4):
        return "Test search"

print("Creating OKF Graph...")
graph = BhagvadOKFGraph()
print("✅ All initialization complete!")
