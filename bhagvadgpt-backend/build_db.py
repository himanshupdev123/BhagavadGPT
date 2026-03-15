import json
import chromadb

print("Hare Krishna! Initializing the BhagvadGPT Database Builder...")

# 1. Load the unified JSON data
try:
    with open("all_verses.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    print(f"Successfully loaded {len(raw_data)} verses from all_verses.json.")
except FileNotFoundError:
    print("❌ Error: all_verses.json not found. Please ensure it is in the same folder.")
    exit()

# 2. Setup the local ChromaDB Persistent Client
# This creates a folder that acts as your offline database.
client = chromadb.PersistentClient(path="./gita_knowledge_base")

# Get or create the collection (the 'table' holding our verses)
collection = client.get_or_create_collection(name="bhagavad_gita")

documents = []
metadatas = []
ids = []

print("Processing verses and generating vector embeddings...")

# 3. Process each verse according to our structural plan
for item in raw_data:
    # Safely extract modern themes, defaulting to an empty list if missing
    themes_list = item.get('modern_themes', [])
    themes_str = ", ".join(themes_list)
    
    # SEARCHABLE DOCUMENT: This is what the AI physically searches through. 
    # We combine themes, the custom purport, and the English translation.
    searchable_text = f"Themes: {themes_str}. Purport: {item.get('purport', '')} Translation: {item.get('translation', '')}"
    
    documents.append(searchable_text)
    
    # ID: A unique identifier for the database row
    ids.append(item.get('reference', f"BG_{item.get('chapter')}_{item.get('verse')}"))
    
    # METADATA: This is attached to the result but NOT searched. 
    # This prevents the embedding model from being confused by Sanskrit characters.
    metadatas.append({
        "shloka": item.get('shloka', ''),
        "reference": item.get('reference', ''),
        "chapter": item.get('chapter', 0),
        "verse": item.get('verse', 0)
    })

# 4. Inject the data into ChromaDB
# This step automatically downloads a small, highly efficient embedding model 
# to convert the English text into searchable mathematical vectors.
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("✅ Divine wisdom successfully embedded! The 'gita_knowledge_base' is ready.")