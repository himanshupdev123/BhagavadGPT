# BhagavadGPT Backend - Project Structure

## 📂 Directory Organization

```
bhagvadgpt-backend/
├── 📁 backups/              # Prompt template version backups
│   ├── README.md            # Backup documentation
│   ├── actualprompt_backup_before_gemini_fixes.txt  # Pre-Gemini version
│   └── actualprompt*.txt    # Earlier backups
│
├── 📁 docs/                 # Implementation documentation
│   ├── README.md            # Documentation index
│   ├── GEMINI_FIXES_APPLIED.md          # Latest: Security optimizations
│   ├── INJECTION_DEFENSE_IMPLEMENTATION.md
│   ├── RESPONSE_LENGTH_IMPLEMENTATION.md
│   └── TASK_*.md            # Task implementation summaries
│
├── 📁 gita_knowledge_base/  # ChromaDB vector database
│   ├── chroma.sqlite3       # Vector storage
│   └── [collection data]
│
├── 📁 venv/                 # Python virtual environment
│
├── 🐍 Core Python Files
│   ├── main.py              # FastAPI server + Enhanced prompt template
│   ├── build_db.py          # ChromaDB builder from all_verses.json
│   └── requirements.txt     # Python dependencies
│
├── 🧪 Test Files
│   ├── test_injection_defense.py
│   ├── test_response_length.py
│   ├── test_response_length_functional.py
│   ├── test_enhanced_prompt_integration.py
│   ├── test_main_integration.py
│   ├── test_prompt_deployment.py
│   ├── test_checkpoint_manual.py
│   ├── run_checkpoint_tests.py
│   └── test_cases_checkpoint.json
│
└── 📄 Configuration Files
    ├── .env                 # API keys (gitignored)
    ├── .env.example         # Environment template
    ├── .gitignore           # Git ignore rules
    ├── all_verses.json      # Source Gita verses (700 verses)
    └── ritam_prompt         # [Legacy prompt file]
```

---

## 🎯 Key Files Explained

### **main.py** (Core Server)
The heart of the backend containing:
- FastAPI server setup with CORS
- API key rotation system (5 Groq API keys)
- ChromaDB connection
- **Enhanced prompt template** with Gemini security fixes
- `/v1/chat/completions` endpoint (OpenAI-compatible)
- Rate limit handling and error recovery

**Key Components**:
- Line ~98: Prompt template definition
- Line ~1204: ChromaDB query (`n_results=5` - retrieves 5 most relevant verses)
- Line ~1200: `/v1/chat/completions` endpoint handler

---

### **build_db.py** (Database Builder)
Builds the ChromaDB vector database from `all_verses.json`:
- Reads all 700 Bhagavad Gita verses
- Generates embeddings using sentence-transformers
- Stores in local ChromaDB collection
- Run once during setup: `python build_db.py`

---

### **all_verses.json** (Source Data)
Contains all 700 verses of the Bhagavad Gita in JSON format:
```json
{
  "chapter": 2,
  "verse": 47,
  "shloka": "कर्मण्येवाधिकारस्ते...",
  "translation": "You have the right to perform...",
  "meaning": "Detailed explanation..."
}
```

---

### **docs/** (Implementation Docs)
All task implementation summaries and verification reports:
- **GEMINI_FIXES_APPLIED.md**: Latest security optimizations (June 26, 2026)
- **TASK_*.md**: Implementation details for each completed task
- See `docs/README.md` for detailed guide

---

### **backups/** (Version Control)
Prompt template backups for rollback:
- **actualprompt_backup_before_gemini_fixes.txt**: Pre-Gemini enhanced version (60KB)
- Earlier backups for historical reference
- See `backups/README.md` for rollback instructions

---

### **Test Files** (Quality Assurance)
Comprehensive test suite covering:
- **Injection defense**: `test_injection_defense.py`
- **Response length**: `test_response_length*.py`
- **Integration**: `test_*_integration.py`
- **Deployment**: `test_prompt_deployment.py`
- **Checkpoint**: Manual testing with real questions

---

## 🔧 Setup & Usage

### Initial Setup
```bash
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
copy .env.example .env
# Edit .env with your Groq API keys

# 4. Build vector database
python build_db.py

# 5. Start server
python main.py
# Server runs at http://localhost:8000
```

### Running Tests
```bash
# Individual test files
python test_injection_defense.py
python test_response_length.py

# Integration tests
python test_main_integration.py

# Manual checkpoint tests
python run_checkpoint_tests.py
```

---

## 📊 Current Status

### ✅ Completed Features
- 6-layer prompt architecture
- Prompt injection defense with XML enclosure
- Multilingual support (14+ languages)
- Response length customization
- Edge case handling (birthdays, follow-ups, relationships, etc.)
- Quality validation checklist (silent)
- Critical reminder anchor
- API key rotation (5 keys)
- Rate limit handling

### 🎯 Key Metrics
- **Prompt length**: ~49,500 characters
- **Database**: 700 Bhagavad Gita verses
- **Retrieval**: 5 verses per query (configurable)
- **API keys**: 5 (from different accounts)
- **Response format**: OpenAI-compatible

### 🔐 Security Features
- XML enclosure for user input isolation
- Silent checklist (prevents leakage)
- Injection pattern detection
- Identity reinforcement

---

## 🚀 Deployment Checklist

Before deploying to production:

1. ✅ All Gemini fixes applied
2. ✅ Prompt template tested
3. ✅ Integration tests pass
4. ⏳ Set up all 5 Groq API keys in `.env`
5. ⏳ Build ChromaDB with `python build_db.py`
6. ⏳ Test with real user queries
7. ⏳ Monitor response quality
8. ⏳ Set up error logging
9. ⏳ Configure CORS for production domain

---

## 📚 Related Documentation

- **Spec documents**: `../../.kiro/specs/enhanced-prompt-system/`
  - `requirements.md` - Complete requirements
  - `design.md` - Architecture and design
  - `tasks.md` - Implementation task list

- **Implementation docs**: `docs/`
- **Backup versions**: `backups/`
- **Main codebase**: BhagavadGPT-frontend/ (parent directory)

---

## 🤝 Contributing

When making changes:
1. Create a backup in `backups/` before major prompt changes
2. Document changes in `docs/`
3. Update this PROJECT_STRUCTURE.md if directory structure changes
4. Run test suite before committing
5. Update requirements.txt if adding dependencies

---

**Last Updated**: June 26, 2026  
**Version**: Enhanced Prompt System with Gemini Security Fixes  
**Status**: Production Ready ✅
