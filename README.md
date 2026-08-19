<img width="1280" height="456" alt="BhagvadGPT Banner" src="https://github.com/user-attachments/assets/1c77ee30-44bc-44e7-946a-0f7ca57f6919" />

# BhagvadGPT

[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/himanshupdev123/BhagavadGPT)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Node](https://img.shields.io/badge/Node-20+-green)](https://nodejs.org)
[![Docker](https://img.shields.io/badge/Docker-Required-blue)](https://docker.com)

**BhagvadGPT** is an AI-powered spiritual companion that retrieves relevant verses from the Bhagavad Gita and provides personalized, contextual guidance — in English, Hindi, and 10+ other Indian languages.

> *"You have the right to work, but never to the fruit of work."* — Bhagavad Gita 2.47

---

## Table of Contents

- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Step 1 — Clone the Repository](#step-1--clone-the-repository)
- [Step 2 — Get API Keys](#step-2--get-api-keys)
- [Step 3 — Backend Setup](#step-3--backend-setup)
- [Step 4 — Frontend Setup](#step-4--frontend-setup)
- [Step 5 — Google Sheets Sync (Optional)](#step-5--google-sheets-sync-optional)
- [Step 6 — Start Everything](#step-6--start-everything)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Configuration Reference](#configuration-reference)
- [Knowledge Base Management](#knowledge-base-management)
- [Capacity & Scaling](#capacity--scaling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## How It Works

When a user sends a message:

1. **Language detection** — if not English, the query is translated for search
2. **Fast tag match** — query words are matched directly against a priority index (zero latency)
3. **LLM tag extraction** — if fast match fails, an LLM picks the most relevant tags from 143 curated options
4. **Priority index lookup** — your hand-curated list determines which shlokas appear first
5. **Verse retrieval** — relevant shlokas are pulled from the in-memory OKF knowledge graph
6. **Response generation** — a Groq LLM generates a personalized response with the verse, Sanskrit, translation, and guidance
7. **Streaming** — the response streams token-by-token to the user

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  BhagvadGPT Frontend                         │
│           (LibreChat — React + TypeScript)                   │
│                                                              │
│   Custom branding · Google OAuth · Streaming chat UI         │
└──────────────────────┬───────────────────────────────────────┘
                       │ OpenAI-compatible API  (Port 3080 → 8000)
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                  BhagvadGPT Backend (FastAPI)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               Request Pipeline                       │   │
│  │                                                      │   │
│  │  Query → Translate → Fast Tag Match                 │   │
│  │                           ↓ (miss)                  │   │
│  │                      LLM Tag Extract                │   │
│  │                           ↓                         │   │
│  │             Priority Index Lookup (Google Sheets)   │   │
│  │                           ↓ (miss)                  │   │
│  │              Semantic Tag Search (OKF Graph)        │   │
│  │                           ↓                         │   │
│  │                    Format Context                   │   │
│  │                           ↓                         │   │
│  │              Groq LLM → Stream Response             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  In-memory OKF Graph: 700 verses · 143 tags · priority index │
│  50 Groq API keys rotating · 750 messages/minute capacity    │
└──────────────────────────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌─────────▼───────┐
│   MongoDB      │          │  Google Sheets  │
│  (chat history)│          │  (tag & shloka  │
│                │          │   curation)     │
└────────────────┘          └─────────────────┘
```

---

## Prerequisites

| Software | Version | Download | Purpose |
|----------|---------|----------|---------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) | Backend |
| Node.js | 20+ | [nodejs.org](https://nodejs.org/) | Frontend build |
| Docker Desktop | Latest | [docker.com](https://www.docker.com/get-docker/) | Frontend services |
| Git | Latest | [git-scm.com](https://git-scm.com/downloads) | Clone repo |

Check what you have:

```bash
python --version    # need 3.10+
node --version      # need 20+
docker --version    # need 20+
git --version
```

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/himanshupdev123/BhagavadGPT.git
cd BhagavadGPT
```

---

## Step 2 — Get API Keys

You need two things: Groq API keys for the AI, and Google OAuth for login.

### Groq API Keys

1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up or log in
3. Click **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)
5. Repeat to create as many keys as you want — more keys = more capacity

Each free Groq key gives you 30 requests/minute and 14,400/day. With 50 keys you can handle 750 messages/minute.

### Google OAuth Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new project named `BhagvadGPT`
3. Go to **APIs & Services → Credentials**
4. Click **Configure Consent Screen** → External → fill in app name and your email → Save
5. Go back to **Credentials → Create Credentials → OAuth 2.0 Client IDs**
6. Application type: **Web application**
7. Add Authorized Redirect URI:
   ```
   https://yourdomain.com/oauth/google/callback
   ```
   For local dev:
   ```
   http://localhost:3080/oauth/google/callback
   ```
8. Copy your **Client ID** and **Client Secret**

---

## Step 3 — Backend Setup

```bash
cd bhagvadgpt-backend
```

### Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create your .env file

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Now open `.env` and fill in your values:

```env
# ── Groq API Keys ──────────────────────────────────────────
# Add as many as you have. Keys are rotated automatically.
GROQ_API_KEY1=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY2=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY3=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ... add more with GROQ_API_KEY4, GROQ_API_KEY5, etc.
# You can also use named keys:
# Contributor_Name=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Google Sheets Sync (optional — see Step 5) ─────────────
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SHEETS_SYNC_INTERVAL=1800
```

### Start the backend

```bash
# Windows (recommended — handles encoding)
start_backend.bat

# Or directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Verify it's running:

```
http://localhost:8000/docs
```

You should see the FastAPI docs page with all available endpoints.

**Keep this terminal open.** The backend must stay running.

---

## Step 4 — Frontend Setup

Open a **new terminal**.

```bash
cd BhagavadGPT-frontend
```

### Create your .env file

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `BhagavadGPT-frontend/.env` and configure:

```env
#──────────────────────────────────────────────────────────────
# Server
#──────────────────────────────────────────────────────────────
HOST=0.0.0.0
PORT=3080

# MongoDB — used for storing chat history
MONGO_URI=mongodb://mongodb:27017/LibreChat

# Your domain (use localhost for local dev)
DOMAIN_CLIENT=http://localhost:3080
DOMAIN_SERVER=http://localhost:3080

#──────────────────────────────────────────────────────────────
# Backend connection
#──────────────────────────────────────────────────────────────
ENDPOINTS=bhagvadgpt
BHAGVADGPT_API_KEY=dummy_key
BHAGVADGPT_BASE_URL=http://host.docker.internal:8000

#──────────────────────────────────────────────────────────────
# Auth secrets
# Generate all 4 values at: https://www.librechat.ai/toolkit/creds_generator
#──────────────────────────────────────────────────────────────
SESSION_EXPIRY=900000
REFRESH_TOKEN_EXPIRY=604800000
JWT_SECRET=REPLACE_WITH_GENERATED_VALUE
JWT_REFRESH_SECRET=REPLACE_WITH_GENERATED_VALUE
CREDS_KEY=REPLACE_WITH_GENERATED_VALUE
CREDS_IV=REPLACE_WITH_GENERATED_VALUE

#──────────────────────────────────────────────────────────────
# Registration
#──────────────────────────────────────────────────────────────
ALLOW_EMAIL_LOGIN=false
ALLOW_REGISTRATION=false
ALLOW_SOCIAL_LOGIN=true
ALLOW_SOCIAL_REGISTRATION=true
ALLOW_UNVERIFIED_EMAIL_LOGIN=false

#──────────────────────────────────────────────────────────────
# Google OAuth
#──────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_CALLBACK_URL=/oauth/google/callback

#──────────────────────────────────────────────────────────────
# Search (MeiliSearch)
#──────────────────────────────────────────────────────────────
SEARCH=true
MEILI_NO_ANALYTICS=true
MEILI_HOST=http://meilisearch:7700
MEILI_MASTER_KEY=generate_a_random_32_char_string_here

#──────────────────────────────────────────────────────────────
# UI
#──────────────────────────────────────────────────────────────
APP_TITLE=BhagvadGPT
HELP_AND_FAQ_URL=https://github.com/himanshupdev123/BhagavadGPT

#──────────────────────────────────────────────────────────────
# Debug
#──────────────────────────────────────────────────────────────
DEBUG_LOGGING=false
DEBUG_CONSOLE=false
```

**Important notes:**
- Generate the 4 auth secrets at [librechat.ai/toolkit/creds_generator](https://www.librechat.ai/toolkit/creds_generator)
- `BHAGVADGPT_BASE_URL` uses `host.docker.internal` so the Docker container can reach your backend running on your machine
- For production, replace all `localhost` references with your actual domain

### Build the Docker image

The first time only, build the custom frontend image:

```bash
docker compose build --no-cache api
```

This takes 5-15 minutes as it compiles the React frontend.

### Start all services

```bash
docker compose up -d
```

This starts:
- `api` — the LibreChat frontend (port 3080)
- `mongodb` — chat history database (port 27017)
- `meilisearch` — search index (port 7700)
- `vectordb` — pgvector for RAG (port 5432)
- `rag_api` — RAG service (port 8000 internal)

Check they're all running:

```bash
docker compose ps
```

All services should show as `running`.

---

## Step 5 — Google Sheets Sync (Optional)

This lets you curate tags and priority shlokas from a Google Sheet, which then sync into the backend automatically.

### What the sheet controls

The Google Sheet has 3 tabs:

| Tab | Purpose |
|-----|---------|
| `Tags` | Maps each verse (e.g. `2.47`) to a list of tags |
| `Related` | Maps each verse to related verses |
| `PriorityIndex` | Maps each tag to an ordered list of shlokas to serve |

The `PriorityIndex` tab is the most powerful — it lets you hand-curate which shloka appears first for any topic.

### Setup

1. Create a Google Sheet with 3 tabs: `Tags`, `Related`, `PriorityIndex`

2. **Tags tab format:**
   ```
   Column A: verse ref (e.g. 2.47)
   Column B onwards: tag1, tag2, tag3, ...
   ```

3. **Related tab format:**
   ```
   Column A: verse ref (e.g. 2.47)
   Column B onwards: related verse refs (e.g. 2.38, 3.19)
   ```

4. **PriorityIndex tab format:**
   ```
   Column A: tag name (e.g. anger)    ← Row 1 is header
   Column B: Priority 1 shloka (e.g. 2.63)
   Column C: Priority 2 shloka (e.g. 3.37)
   Column D: Priority 3 shloka ...
   ```

5. Create a Google Cloud service account:
   - Go to [console.cloud.google.com](https://console.cloud.google.com/)
   - Enable the **Google Sheets API**
   - Create a service account under **IAM & Admin → Service Accounts**
   - Download the JSON key file
   - Save it as `bhagvadgpt-backend/bhagvadgpt_okf/service-account.json`

6. Share your Google Sheet with the service account email (Viewer access)

7. Add to `bhagvadgpt-backend/.env`:
   ```env
   GOOGLE_SHEET_ID=your_sheet_id_from_the_url
   ```

8. Manual sync whenever you update the sheet:
   ```bash
   cd bhagvadgpt-backend
   python sync_and_write_files_v2.py
   ```
   Or hit the API endpoint:
   ```
   GET http://localhost:8000/api/sync-sheets
   ```

The backend also syncs once automatically on startup.

---

## Step 6 — Start Everything

### Checklist before starting

- [ ] Backend `.env` has at least one valid `GROQ_API_KEY1`
- [ ] Frontend `.env` has `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- [ ] Frontend `.env` has all 4 auth secrets generated
- [ ] Docker Desktop is running

### Start order

1. Start the backend first:
   ```bash
   cd bhagvadgpt-backend
   venv\Scripts\activate     # Windows
   .\start_backend.bat
   ```

2. Start the frontend:
   ```bash
   cd BhagavadGPT-frontend
   docker compose up -d
   ```

3. Open the app:
   ```
   http://localhost:3080
   ```

### Convenience scripts (root folder)

```bash
start_bhagvadgpt.bat    # starts both backend and frontend
stop_bhagvadgpt.bat     # stops everything
```

---

## API Reference

The backend exposes an OpenAI-compatible API plus BhagvadGPT-specific management endpoints.

### Chat

```http
POST /v1/chat/completions
Content-Type: application/json

{
  "messages": [{"role": "user", "content": "I feel very anxious about exams"}],
  "stream": true,
  "model": "bhagvadgpt"
}
```

Supports both `stream: true` (token-by-token) and `stream: false` (full response).

### Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sync-sheets` | Manually trigger sync from Google Sheets |
| GET | `/api/sync-status` | Check last sync time and status |
| GET | `/api/key-stats` | API key rotation statistics |
| GET | `/api/question-stats` | Total questions answered |
| GET | `/api/question-count` | Simple count for the login page counter |

### Example: Check system status

```bash
curl http://localhost:8000/api/sync-status
```

```json
{
  "available": true,
  "sheet_id": "...",
  "last_sync_time": "2026-08-19 10:30:00",
  "verses_loaded": 700
}
```

---

## Project Structure

```
BhagavadGPT/
│
├── bhagvadgpt-backend/                  ← Python FastAPI backend
│   ├── main.py                          ← Core server: all API endpoints + search logic
│   ├── google_sheets_sync.py            ← Fetches tags, related, priority index from Sheets
│   ├── requirements.txt                 ← Python dependencies
│   ├── start_backend.bat                ← Windows start script
│   ├── .env                             ← API keys and config (never commit this)
│   ├── .env.example                     ← Template for .env
│   │
│   ├── bhagvadgpt_okf/                  ← 700 verse markdown files
│   │   ├── chapter_1/
│   │   │   ├── verse_1.md               ← Each file = one shloka with frontmatter
│   │   │   └── verse_2.md
│   │   ├── chapter_2/
│   │   └── ... (18 chapters)
│   │
│   ├── 100_MASTER_TAGS.txt              ← Old master tag list (514 tags)
│   ├── PRIORITY_TAGS_FOR_EXCEL.txt      ← 143 curated tags for PriorityIndex
│   ├── question_tag_dataset.csv         ← Training data: questions → tags
│   ├── tag_shloka_dataset.csv           ← Training data: tags → shlokas
│   ├── questions_list.txt               ← All real user questions logged
│   │
│   ├── sync_and_write_files_v2.py       ← Sync Google Sheets → markdown files
│   ├── generate_training_dataset.py     ← Generate question→tag training CSV
│   ├── generate_tag_shloka_dataset.py   ← Generate tag→shloka training CSV
│   ├── generate_priority_tags.py        ← Analyze questions to suggest new tags
│   ├── enrich_tags.py                   ← LLM-enriches tags on existing verses
│   │
│   ├── question_counter.json            ← Persisted counter of answered questions
│   └── venv/                            ← Python virtual environment
│
├── BhagavadGPT-frontend/                ← LibreChat-based frontend
│   ├── client/
│   │   └── src/
│   │       └── components/
│   │           └── Auth/
│   │               └── Login.tsx        ← Custom login page (Google only + counter)
│   ├── librechat.yaml                   ← BhagvadGPT model + UI configuration
│   ├── docker-compose.yml               ← Service definitions
│   ├── docker-compose.override.yml      ← Builds from local Dockerfile
│   ├── Dockerfile                       ← Frontend container build
│   ├── .env                             ← Frontend config (OAuth, secrets, URLs)
│   └── .env.example                     ← Template for .env
│
├── gita_knowledge_base/                 ← ChromaDB vector store (legacy)
├── start_bhagvadgpt.bat                 ← Start everything (Windows)
├── stop_bhagvadgpt.bat                  ← Stop everything (Windows)
├── LICENSE
└── README.md
```

### Verse file format

Each shloka is a markdown file with YAML frontmatter:

```markdown
---
type: shloka
title: Chapter 2, Verse 47
tags:
  - duty
  - detachment from results
  - karma
related:
  - chapter_3/verse_19
  - chapter_18/verse_66
chapter: 2
verse_number: 47
speaker: Krishna
---

# Chapter 2, Verse 47

**Sanskrit (Devanagari):**
कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।

**English Translation:**
You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions.

**Meaning & Purport:**
...
```

---

## Configuration Reference

### Backend `.env` keys

| Key | Required | Description |
|-----|----------|-------------|
| `GROQ_API_KEY1` ... `GROQ_API_KEYn` | Yes | Groq API keys. Name any number sequentially. |
| `GOOGLE_SHEET_ID` | Optional | Google Sheets ID for tag/priority sync |
| `GOOGLE_SHEETS_SYNC_INTERVAL` | Optional | Seconds between auto-syncs (default: 1800) |

### Frontend `.env` keys

| Key | Required | Description |
|-----|----------|-------------|
| `MONGO_URI` | Yes | MongoDB connection string |
| `DOMAIN_CLIENT` | Yes | Your frontend URL |
| `DOMAIN_SERVER` | Yes | Your backend URL |
| `BHAGVADGPT_BASE_URL` | Yes | URL to the Python backend |
| `JWT_SECRET` | Yes | Random secret for JWT tokens |
| `JWT_REFRESH_SECRET` | Yes | Random secret for refresh tokens |
| `CREDS_KEY` | Yes | 32-byte encryption key |
| `CREDS_IV` | Yes | 16-byte encryption IV |
| `GOOGLE_CLIENT_ID` | Yes | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | Google OAuth client secret |
| `MEILI_MASTER_KEY` | Yes | MeiliSearch master key (any random string) |
| `APP_TITLE` | Optional | Browser tab title (default: BhagvadGPT) |

### librechat.yaml

Located at `BhagavadGPT-frontend/librechat.yaml`. Controls:
- Which endpoints are available (locked to `bhagvadgpt`)
- UI elements shown/hidden (model selector, sidebar, etc.)
- Social login providers (`google` only)
- Model display settings and token limits

---

## Knowledge Base Management

### Sync from Google Sheets

After updating your Google Sheet:

```bash
cd bhagvadgpt-backend
python sync_and_write_files_v2.py
```

Or via API (syncs the live backend without restart):

```
GET http://localhost:8000/api/sync-sheets
```

### Enrich tags with LLM

For chapters 1-6 verses that already have some tags, let the LLM suggest additional ones:

```bash
python enrich_tags.py
```

### Generate training datasets

```bash
# Map real user questions to tags
python generate_training_dataset.py
# Output: question_tag_dataset.csv

# Map tags to shlokas
python generate_tag_shloka_dataset.py
# Output: tag_shloka_dataset.csv
```

### Suggest new tags from user questions

```bash
python generate_priority_tags.py
# Output: PRIORITY_TAGS_FOR_EXCEL.txt
```

### Rebuild the frontend after code changes

```bash
cd BhagavadGPT-frontend
docker compose build --no-cache api
docker compose up -d
```

---

## Capacity & Scaling

With 50 Groq free-tier API keys:

| Metric | Value |
|--------|-------|
| API keys | 50 |
| Requests per minute (total) | 1,500 |
| Messages per minute (2 calls/msg) | 750 |
| Messages per day | 360,000 |
| Latency per response | 7-15 seconds |
| Concurrent chatting users (no wait) | ~375 |

Each API key gives 30 RPM and 14,400 requests/day on Groq free tier. Keys rotate automatically — if one hits rate limit, the next is used instantly.

**To add more keys:** Add `GROQ_API_KEY6=gsk_...`, `GROQ_API_KEY7=gsk_...`, etc. to `.env`. The backend picks them all up on startup.

**To scale the server:** Run uvicorn with multiple workers:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Troubleshooting

### Backend won't start — encoding error on Windows

```bash
# Run with UTF-8 mode
set PYTHONUTF8=1 && uvicorn main:app --host 0.0.0.0 --port 8000
# Or just use the bat file:
.\start_backend.bat
```

### Frontend can't reach backend

Check `BHAGVADGPT_BASE_URL` in `BhagavadGPT-frontend/.env`. Inside Docker it should be:
```
BHAGVADGPT_BASE_URL=http://host.docker.internal:8000
```
Not `localhost` — Docker containers can't reach `localhost` on your machine.

### Google login doesn't work

1. Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in frontend `.env`
2. In Google Cloud Console, check the redirect URI matches exactly:
   ```
   https://yourdomain.com/oauth/google/callback
   ```
3. Make sure the app is not in "Testing" mode with restricted users

### Docker build fails with memory error

```bash
# Increase Node memory limit
docker compose build --build-arg NODE_MAX_OLD_SPACE_SIZE=4096 api
```

### Response takes 15+ seconds

This is expected with reasoning models on the free Groq tier. The pipeline:
- Fast tag match: ~0ms
- LLM tag extraction (fallback): ~3-5s
- Main LLM response: ~7-12s

To reduce latency, ensure your question contains recognizable tag keywords (e.g. "angry", "sad", "anxious") so the fast path is used.

### Google Sheets sync fails

1. Confirm `GOOGLE_SHEET_ID` is correct (from the sheet URL: `.../d/SHEET_ID/edit`)
2. Check the service account JSON is at `bhagvadgpt_okf/service-account.json`
3. Confirm the service account email has Viewer access to the sheet

### Port already in use

```bash
# Windows — find what's using port 8000
netstat -ano | findstr :8000
# Kill it by PID
taskkill /F /PID <PID>
```

### View Docker logs

```bash
cd BhagavadGPT-frontend
docker compose logs -f api        # frontend logs
docker compose logs -f mongodb    # database logs
```

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make changes and test locally
4. Commit: `git commit -m "Add: description"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

### Ways to contribute

- Add Groq API keys to increase capacity
- Tag more verses in the Google Sheet (chapters 7-18 need work)
- Fill in the PriorityIndex for more tags
- Add test questions to `questions_list.txt`
- Report bugs or UX issues

---

## License

MIT License — see [LICENSE](LICENSE). Free to use, modify, and distribute.

---

## Acknowledgments

- The Bhagavad Gita — the eternal source of this wisdom
- [LibreChat](https://github.com/danny-avila/LibreChat) — open-source chat UI
- [Groq](https://groq.com/) — fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) — Python API framework
- All contributors who shared their Groq API keys

---

**Radhe Radhe 🙏**

*"The soul is neither born, nor does it ever die."* — Bhagavad Gita 2.20
