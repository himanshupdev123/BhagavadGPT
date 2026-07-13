# BhagavadGPT Backend

FastAPI backend for BhagavadGPT - An AI-powered spiritual guide based on the Bhagavad Gita using OKF (Open Knowledge Format) knowledge graph.

## 🌟 Features

- **OKF Knowledge Graph**: 700 verses loaded in memory with tag-based semantic search
- **Related Field Traversal**: Automatically includes contextually connected verses
- **Token Optimization**: Smart context building that stays under API limits
- **Multi-key Rotation**: 5 Groq API keys for rate limit management
- **Streaming Responses**: OpenAI-compatible API with streaming support
- **Security**: Prompt injection defense and input validation

## 📁 Project Structure

```
BhagavadGPT/bhagvadgpt-backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
├── .env.example         # Example environment file
│
├── bhagvadgpt_okf/      # OKF verse files (700 markdown files)
│   ├── chapter_1/
│   ├── chapter_2/
│   └── ...
│
├── docs/                # All documentation
│   ├── README.md
│   ├── OKF_RELATED_FIELD.md
│   ├── KNOWLEDGE_GRAPH_IMPLEMENTATION.md
│   ├── TESTING_GUIDE.md
│   └── ...
│
├── tests/               # Test suite
│   ├── README.md
│   ├── test_okf_complete.py
│   ├── test_related_traversal.py
│   ├── test_full_integration.py
│   └── ...
│
├── scripts/             # Utility scripts
│   ├── README.md
│   ├── migrate_to_okf.py
│   ├── enhance_okf_tags.py
│   └── ...
│
├── backups/             # Backup files
└── venv/                # Python virtual environment
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd BhagavadGPT/bhagvadgpt-backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your Groq API keys:

```bash
GROQ_API_KEY1=your_first_key_here
GROQ_API_KEY2=your_second_key_here
GROQ_API_KEY3=your_third_key_here
GROQ_API_KEY4=your_fourth_key_here
GROQ_API_KEY5=your_fifth_key_here
```

### 3. Run Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 4. Test API

```powershell
# PowerShell
$body = '{"messages":[{"role":"user","content":"How to overcome fear?"}],"stream":false,"model":"bhagvadgpt"}'
Invoke-RestMethod -Uri "http://localhost:8000/v1/chat/completions" -Method Post -ContentType "application/json" -Body $body
```

## 🧪 Testing

### Run All Tests
```bash
# Complete system test
python tests/test_okf_complete.py

# Integration test
python tests/test_full_integration.py

# Related field traversal
python tests/test_related_traversal.py
python tests/test_related_detailed.py
```

### Expected Results
```
✅ 700 verses loaded
✅ 676 verses with tags (96.6%)
✅ 297 verses with related connections (42.4%)
✅ Graph traversal working
✅ All tests passing
```

## 📊 System Statistics

- **Total verses**: 700
- **Tagged verses**: 676 (96.6%)
- **Connected verses**: 297 (42.4%)
- **Total connections**: 893
- **Average tags/verse**: 11.7
- **Load time**: 1-2 seconds
- **Search time**: <100ms
- **Memory usage**: ~57MB

## 🔧 API Endpoints

### Chat Completion (OpenAI Compatible)

```http
POST /v1/chat/completions
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your question here"}
  ],
  "stream": false,
  "model": "bhagvadgpt"
}
```

**Response:**
```json
{
  "id": "chatcmpl-bhagvadgpt",
  "object": "chat.completion",
  "model": "bhagvadgpt",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Namaste! To your situation..."
    },
    "finish_reason": "stop"
  }]
}
```

### Key Statistics

```http
GET /api/key-stats
```

Returns API key rotation statistics.

## 🏗️ Architecture

### OKF Knowledge Graph

```
User Query
    ↓
Tag-Based Search (700 verses)
    ↓
Select Top K Primary Matches
    ↓
Traverse Related Field
    ↓
Fetch Related Verses
    ↓
Build Context (Primary + Related)
    ↓
Send to LLM
    ↓
Stream Response to User
```

### Key Components

1. **BhagvadOKFGraph**: In-memory knowledge graph
   - Tag-based semantic search
   - Related field traversal
   - Token-efficient context building

2. **API Key Rotation**: Smart rotation of 5 Groq API keys
   - Automatic failover on rate limits
   - Cooldown period tracking
   - Usage statistics

3. **Prompt Template**: 6-layer architecture
   - Input validation
   - Safety overrides
   - Context formatting
   - Response generation

## 📚 Documentation

- **[OKF Related Field](docs/OKF_RELATED_FIELD.md)** - How the knowledge graph works
- **[Implementation Guide](docs/KNOWLEDGE_GRAPH_IMPLEMENTATION.md)** - Technical details
- **[Testing Guide](docs/TESTING_GUIDE.md)** - How to run tests
- **[Graph Flow](docs/GRAPH_TRAVERSAL_FLOW.md)** - Visual architecture

## 🛠️ Utility Scripts

Located in `scripts/` folder:

- **migrate_to_okf.py** - Migrate from ChromaDB to OKF
- **enhance_okf_tags.py** - Enhance tags with user-query language
- **refine_tags_v2.py** - Advanced tag refinement

## 🔐 Security

- Prompt injection defense
- Input validation and sanitization
- Suicide/self-harm override
- Violence/harm detection
- Out-of-domain filtering

## 📝 Requirements

```
fastapi
uvicorn
python-dotenv
langchain-groq
langchain-core
pyyaml
groq
```

## 🌐 Current Model

**Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- Temperature: 0.6
- Provider: Groq Cloud
- Token Limit: 8000

## 🤝 Integration

Compatible with LibreChat frontend via OpenAI-compatible API.

## 📈 Performance

- Fast in-memory retrieval: <100ms
- Token-efficient: 500-900 words per query
- Context enrichment: 30-50% more verses via related field
- Handles high volume with 5-key rotation

## 🐛 Troubleshooting

**Issue**: "Module not found"
```bash
pip install -r requirements.txt
```

**Issue**: "API key invalid"
- Check `.env` file has valid Groq API keys
- Visit https://console.groq.com for new keys

**Issue**: "No verses loaded"
- Ensure `bhagvadgpt_okf/` directory exists with verse files
- Run `python scripts/migrate_to_okf.py` if needed

## 📞 Support

See documentation in `docs/` folder for detailed guides.

## ✅ Status

**Production Ready**
- All features implemented
- All tests passing
- Documentation complete
- Performance optimized

---

**Last Updated**: July 2026  
**Version**: OKF Knowledge Graph with Related Field Traversal  
**Status**: ✅ Production Ready
