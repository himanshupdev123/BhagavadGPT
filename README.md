#  BhagvadGPT 
<img width="1280" height="456" alt="WhatsApp Image 2026-06-14 at 1 54 39 PM" src="https://github.com/user-attachments/assets/1c77ee30-44bc-44e7-946a-0f7ca57f6919" />


[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/himanshupdev123/BhagavadGPT)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Node](https://img.shields.io/badge/Node-20+-green)](https://nodejs.org)

**BhagvadGPT** is an AI-powered spiritual companion that provides wisdom and guidance based on the teachings of the Bhagavad Gita. Built with modern RAG (Retrieval-Augmented Generation) technology, it retrieves relevant verses from the sacred text and provides personalized spiritual guidance.

> **"You have the right to work, but never to the fruit of work."** - Bhagavad Gita 2.47

---

##  Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Complete Setup Guide](#-complete-setup-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Get API Keys](#step-2-get-api-keys-required)
  - [Step 3: Backend Setup](#step-3-backend-setup)
  - [Step 4: Frontend Setup](#step-4-frontend-setup)
  - [Step 5: Start the Application](#step-5-start-the-application)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎯 **RAG-Powered Responses**: Retrieves relevant verses from the Bhagavad Gita using ChromaDB vector database
- 🤖 **AI-Driven Guidance**: Uses Groq's Llama 3.3 70B model for intelligent, contextual responses
- 🎨 **Custom UI**: Beautiful saffron-themed interface with Om symbol logo
- 🔐 **Google OAuth**: Secure authentication with Google Sign-In
- 💬 **Modern Chat Interface**: Built on LibreChat framework
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 📚 **Complete Gita Database**: All 700+ verses with Sanskrit, translations, and meanings
- 🔄 **API Key Rotation**: Automatic rotation of 5 Groq API keys for higher rate limits
- 🌐 **Multi-language Support**: Hindi, Hinglish, and English responses

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BhagvadGPT Frontend                      │
│              (LibreChat - React + TypeScript)               │
│                                                             │
│  • Custom Branding (Saffron Theme)                         │
│  • Google OAuth Integration                                │
│  • Chat Interface with History                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST API (Port 8000)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 BhagvadGPT Backend                          │
│                  (FastAPI + Python)                         │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  ChromaDB   │───▶│  RAG Engine  │───▶│  Groq LLM    │  │
│  │  (Vectors)  │    │  (Semantic   │    │  (Llama 3.3  │  │
│  │             │    │   Search)    │    │   70B)       │  │
│  └─────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

Before you begin, make sure you have the following installed on your computer:

### Required Software:

| Software | Version | Download Link | Purpose |
|----------|---------|---------------|---------|
| **Python** | 3.10 or higher | [python.org/downloads](https://www.python.org/downloads/) | Backend server |
| **Node.js** | 20 or higher | [nodejs.org](https://nodejs.org/) | Frontend build |
| **MongoDB** | 6.0 or higher | [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) | Database for chat history |
| **Git** | Latest | [git-scm.com/downloads](https://git-scm.com/downloads) | Clone repository |
| **Docker** (Optional) | Latest | [docker.com/get-docker](https://www.docker.com/get-docker/) | Containerized deployment |

### How to Check if Already Installed:

```bash
# Check Python version
python --version
# or
python3 --version

# Check Node.js version
node --version

# Check MongoDB version
mongod --version

# Check Git version
git --version

# Check Docker version (if using Docker)
docker --version
```

If any command returns "command not found", you need to install that software.

---

## 🚀 Complete Setup Guide

Follow these steps **exactly** in order. Do not skip any step.

### Step 1: Clone the Repository

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
# Navigate to where you want to install BhagvadGPT
cd Desktop  # or any folder you prefer

# Clone the repository
git clone https://github.com/himanshupdev123/BhagavadGPT.git

# Enter the project folder
cd BhagavadGPT
```

**Verify**: You should see folders like `bhagvadgpt-backend` and `BhagvadGPT-frontend` when you run `ls` (Mac/Linux) or `dir` (Windows).

---

### Step 2: Get API Keys (Required)

You need **TWO** types of API keys before proceeding:

#### A. Groq API Keys (for AI responses)

1. Go to [console.groq.com](https://console.groq.com/)
2. Click **"Sign Up"** or **"Log In"**
3. After login, click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_...`)
6. **IMPORTANT**: Create **5 API keys** (you can use 5 different email accounts or create multiple keys from one account)

**Why 5 keys?** BhagvadGPT uses API key rotation to handle more users simultaneously.

#### B. Google OAuth Credentials (for user login)

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Click **"Create Project"** (top bar)
3. Name it "BhagvadGPT" and click **"Create"**
4. In the sidebar, go to **"APIs & Services" → "Credentials"**
5. Click **"Configure Consent Screen"**
   - Select **"External"**
   - Fill in:
     - App name: `BhagvadGPT`
     - User support email: Your email
     - Developer contact: Your email
   - Click **"Save and Continue"** → **"Save and Continue"** (skip scopes)
   - Add test users (your email)
   - Click **"Save and Continue"**
6. Go back to **"Credentials"** tab
7. Click **"Create Credentials" → "OAuth 2.0 Client IDs"**
8. Application type: **"Web application"**
9. Name: `BhagvadGPT OAuth`
10. Under **"Authorized redirect URIs"**, click **"Add URI"** and enter:
    ```
    http://localhost:3080/oauth/google/callback
    ```
11. Click **"Create"**
12. Copy your **Client ID** and **Client Secret** (you'll need these soon)

**Save these keys somewhere safe!**

---

### Step 3: Backend Setup

Now we'll set up the Python backend that handles AI responses.

#### 3.1 Navigate to Backend Folder

```bash
# From the BhagavadGPT root folder
cd bhagvadgpt-backend
```

#### 3.2 Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` appear before your command prompt.**

#### 3.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install FastAPI, ChromaDB, LangChain, and other required packages. **Wait for it to complete** (may take 2-3 minutes).

#### 3.4 Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

**On Windows, if `cp` doesn't work:**
```bash
copy .env.example .env
```

#### 3.5 Edit .env File

Open `.env` file in any text editor (Notepad, VSCode, etc.) and add your 5 Groq API keys:

```bash
GROQ_API_KEY1=gsk_your_first_key_here
GROQ_API_KEY2=gsk_your_second_key_here
GROQ_API_KEY3=gsk_your_third_key_here
GROQ_API_KEY4=gsk_your_fourth_key_here
GROQ_API_KEY5=gsk_your_fifth_key_here
```

**Replace** `gsk_your_first_key_here` with your actual Groq API keys from Step 2.

**Save the file.**

#### 3.6 Build the Vector Database

This step creates a searchable database of all Bhagavad Gita verses:

```bash
python build_db.py
```

**Expected output:**
```
Hare Krishna! Initializing the BhagvadGPT Database Builder...
Successfully loaded 700 verses from all_verses.json.
Processing verses and generating vector embeddings...
✅ Divine wisdom successfully embedded! The 'gita_knowledge_base' is ready.
```

This creates a `gita_knowledge_base` folder with the ChromaDB database.

#### 3.7 Test the Backend

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
Initializing BhagvadGPT Backend...
✅ Loaded 5 Groq API keys for rotation
✅ Connected to local Chroma vector database.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test**: Open your browser and go to `http://localhost:8000/docs`. You should see the API documentation.

**Keep this terminal window open** (backend needs to keep running). Open a **new terminal** for the next steps.

---

### Step 4: Frontend Setup

Open a **NEW terminal window/tab** and navigate to the frontend folder.

#### 4.1 Navigate to Frontend Folder

```bash
# From the BhagavadGPT root folder
cd BhagavadGPT-frontend
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

This will take **5-10 minutes** as it installs hundreds of packages. **Be patient!**

#### 4.3 Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

**On Windows, if `cp` doesn't work:**
```bash
copy .env.example .env
```

#### 4.4 Edit Frontend .env File

Open `BhagavadGPT-frontend/.env` in a text editor and configure:

```bash
#==================================================#
#               Server Configuration               #
#==================================================#

HOST=localhost
PORT=3080

# MongoDB (required for LibreChat)
MONGO_URI=mongodb://127.0.0.1:27017/LibreChat

# Your domain
DOMAIN_CLIENT=http://localhost:3080
DOMAIN_SERVER=http://localhost:3080

#===================================================#
#                     Endpoints                     #
#===================================================#

# Point to your local BhagvadGPT backend
ENDPOINTS=bhagvadgpt

# BhagvadGPT endpoint configuration
BHAGVADGPT_API_KEY=dummy_key
BHAGVADGPT_BASE_URL=http://localhost:8000

#===================================================#
#                  Authentication                   #
#===================================================#

# Session secrets - GENERATE YOUR OWN!
# Visit: https://www.librechat.ai/toolkit/creds_generator
# Copy the generated values below:

JWT_SECRET=your_generated_jwt_secret_here
JWT_REFRESH_SECRET=your_generated_jwt_refresh_secret_here
CREDS_KEY=your_generated_creds_key_here
CREDS_IV=your_generated_creds_iv_here

SESSION_EXPIRY=900000
REFRESH_TOKEN_EXPIRY=604800000

#========================#
# Registration and Login #
#========================#

ALLOW_EMAIL_LOGIN=true
ALLOW_REGISTRATION=true
ALLOW_SOCIAL_LOGIN=true
ALLOW_SOCIAL_REGISTRATION=true

#============#
# Google OAuth - ADD YOUR CREDENTIALS HERE
#============#

GOOGLE_CLIENT_ID=your_google_client_id_from_step_2
GOOGLE_CLIENT_SECRET=your_google_client_secret_from_step_2
GOOGLE_CALLBACK_URL=/oauth/google/callback

#==================================================#
#                      Search                      #
#==================================================#

SEARCH=true
MEILI_NO_ANALYTICS=true
MEILI_HOST=http://0.0.0.0:7700
MEILI_MASTER_KEY=your_meili_master_key_generate_random_string

#===================================================#
#                        UI                         #
#===================================================#

APP_TITLE=BhagvadGPT
HELP_AND_FAQ_URL=https://github.com/himanshupdev123/BhagavadGPT
```

**IMPORTANT STEPS:**

1. **Generate Secrets**: Go to [librechat.ai/toolkit/creds_generator](https://www.librechat.ai/toolkit/creds_generator)
   - Copy `JWT_SECRET`, `JWT_REFRESH_SECRET`, `CREDS_KEY`, and `CREDS_IV`
   - Paste them into your `.env` file

2. **Add Google OAuth**: Replace `your_google_client_id_from_step_2` and `your_google_client_secret_from_step_2` with your actual Google OAuth credentials from Step 2.

3. **Generate Meili Key**: Replace `your_meili_master_key_generate_random_string` with any random 32-character string (e.g., use [passwordsgenerator.net](https://passwordsgenerator.net/))

**Save the file.**

#### 4.5 Start MongoDB

**On Windows:**
```bash
# Open a new terminal as Administrator
net start MongoDB
```

**On Mac:**
```bash
brew services start mongodb-community
```

**On Linux:**
```bash
sudo systemctl start mongod
```

**Verify MongoDB is running:**
```bash
mongosh --eval "db.version()"
```

You should see the MongoDB version number.

---

### Step 5: Start the Application

Now we'll start everything using Docker Compose.

#### 5.1 Make Sure Backend is Still Running

Check the terminal where you started the backend (Step 3.7). It should still be running. If not, restart it:

```bash
cd bhagvadgpt-backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 5.2 Start Frontend Services with Docker

In the frontend terminal:

```bash
# Make sure you're in BhagvadGPT-frontend folder
cd BhagavadGPT-frontend

# Start all frontend services
docker-compose up -d
```

**This will:**
- Start MongoDB container
- Start Meilisearch (for chat history search)
- Start LibreChat frontend
- Start the API server

**Expected output:**
```
Creating network "bhagvadgpt-frontend_default" ...
Creating bhagvadgpt-mongodb   ... done
Creating bhagvadgpt-meilisearch ... done
Creating bhagvadgpt-api       ... done
Creating bhagvadgpt-client    ... done
```

**Wait 30-60 seconds** for all services to fully start.

#### 5.3 Verify Everything is Running

```bash
docker-compose ps
```

You should see all services as "Up" (running).

---

### 🎉 Access BhagvadGPT

Open your browser and go to:

```
http://localhost:3080
```

**You should see:**
- BhagvadGPT login page
- "Welcome to BhagvadGPT" header
- Google Sign-In button

**Click "Sign in with Google"** and start your spiritual journey!

---

## ❓ Troubleshooting

### Problem: Backend says "Can't connect to Groq API"

**Solution:**
1. Check your `.env` file in `bhagvadgpt-backend` folder
2. Make sure API keys are valid (test at [console.groq.com](https://console.groq.com/))
3. Restart backend: `Ctrl+C` then run `python -m uvicorn main:app --host 0.0.0.0 --port 8000`

### Problem: Frontend shows "Cannot connect to backend"

**Solution:**
1. Make sure backend is running (check Step 3.7)
2. Verify `BHAGVADGPT_BASE_URL=http://localhost:8000` in frontend `.env`
3. Test backend by visiting `http://localhost:8000/docs` in browser

### Problem: Google login doesn't work

**Solution:**
1. Check Google OAuth credentials in frontend `.env` file
2. Make sure redirect URI in Google Console matches: `http://localhost:3080/oauth/google/callback`
3. Add yourself as a test user in Google Console

### Problem: "Database connection error"

**Solution:**
1. Make sure MongoDB is running: `mongosh --eval "db.version()"`
2. Check `MONGO_URI` in frontend `.env` file
3. Restart MongoDB (see Step 4.5)

### Problem: Docker containers won't start

**Solution:**
1. Make sure Docker is running
2. Stop all containers: `docker-compose down`
3. Remove old containers: `docker-compose rm -f`
4. Rebuild: `docker-compose up -d --build`

### Problem: Port already in use

**Solution:**
1. Check if something is using port 3080 or 8000:
   ```bash
   # Windows
   netstat -ano | findstr :3080
   netstat -ano | findstr :8000
   
   # Mac/Linux
   lsof -i :3080
   lsof -i :8000
   ```
2. Kill the process or change ports in `.env` files

### Still Having Issues?

1. Check the [docs folder](./docs) for detailed documentation
2. Open an issue on [GitHub](https://github.com/himanshupdev123/BhagavadGPT/issues)
3. Include:
   - Error message
   - Operating system
   - Steps you followed
   - Screenshot if possible

---

## 📁 Project Structure

```
BhagavadGPT/
│
├── bhagvadgpt-backend/              # Python FastAPI backend
│   ├── main.py                      # API endpoints & logic
│   ├── build_db.py                  # Vector database builder
│   ├── all_verses.json              # 700+ Gita verses with translations
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Backend configuration (API keys)
│   └── gita_knowledge_base/         # ChromaDB vector storage (auto-generated)
│
├── BhagvadGPT-frontend/             # LibreChat-based frontend
│   ├── client/                      # React frontend application
│   │   ├── src/                     # Source code
│   │   └── public/                  # Static assets (logo, images)
│   ├── api/                         # Backend API for frontend
│   ├── packages/                    # Shared packages
│   ├── librechat.yaml               # BhagvadGPT model configuration
│   ├── docker-compose.yml           # Docker services setup
│   ├── package.json                 # Node dependencies
│   └── .env                         # Frontend configuration (OAuth, secrets)
│
├── docs/                            # Documentation folder
│   ├── SETUP.md                     # Detailed setup guide
│   ├── API_KEY_ROTATION.md          # API key management
│   ├── DEPLOY_HUGGINGFACE.md        # Deployment guides
│   └── ... (other documentation)
│
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## 🛠️ Development

### Run Backend in Development Mode

```bash
cd bhagvadgpt-backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Auto-reload on code changes
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend in Development Mode

```bash
cd BhagvadGPT-frontend

# Start frontend dev server (without Docker)
npm run frontend:dev
```

Frontend will be at `http://localhost:3090` in dev mode.

### View API Documentation

While backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Check API Key Usage

```bash
curl http://localhost:8000/api/key-stats
```

Shows how many times each API key has been used.

---

## 🐳 Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Rebuild containers
```bash
docker-compose up -d --build
```

### Remove all containers and volumes
```bash
docker-compose down -v
```

---

## 🌐 Deployment

See [docs/DEPLOY_HUGGINGFACE.md](./docs/DEPLOY_HUGGINGFACE.md) for deployment guides to:
- Railway.app
- Render.com
- Heroku
- AWS/GCP/Azure
- Hugging Face Spaces

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test locally
5. Commit with clear message:
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a Pull Request on GitHub

### Areas We Need Help:
- 🌍 Translations (Hindi, Sanskrit, other Indian languages)
- 🎨 UI/UX improvements
- 📚 More Gita commentaries (Prabhupada, Vivekananda, etc.)
- 🧪 Testing and bug reports
- 📖 Documentation improvements

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
✅ Free to use for personal or commercial projects  
✅ Modify and distribute  
✅ Include in proprietary software  
❗ Must include original license and copyright notice

---

## 🙏 Acknowledgments

This project is built on the shoulders of giants:

- **Bhagavad Gita** - The eternal source of wisdom (5000+ years old)
- **LibreChat** - Amazing open-source chat UI framework
- **Groq** - Lightning-fast LLM inference
- **ChromaDB** - Efficient vector database for semantic search
- **LangChain** - RAG implementation tools
- **FastAPI** - Modern Python web framework
- **React** - Frontend library
- **MongoDB** - Database for chat history

### Special Thanks:
- A.C. Bhaktivedanta Swami Prabhupada - For his translations and purports
- All contributors who helped make this project possible
- The open-source community

---

## 📧 Contact & Support

- **Developer**: Himanshu P Dev
- **GitHub**: [@himanshupdev123](https://github.com/himanshupdev123)
- **Project**: [github.com/himanshupdev123/BhagavadGPT](https://github.com/himanshupdev123/BhagavadGPT)
- **Issues**: [Report bugs or request features](https://github.com/himanshupdev123/BhagavadGPT/issues)

---

## ⭐ Star This Project

If BhagvadGPT helped you find peace or wisdom, please:
1. **Star this repository** on GitHub ⭐
2. **Share with friends** who might benefit 🙏
3. **Contribute** to make it better for everyone 🤝

---

**Radhe Radhe! 🙏**

*"The soul is neither born, and nor does it die." - Bhagavad Gita 2.20*

*May this tool help you find peace and wisdom in the teachings of the Bhagavad Gita.*

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Status**: Active Development
