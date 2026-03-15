# BhagavadGPT
Coming Soon this Krishna Janmashtami 2026
<img width="1600" height="718" alt="image" src="https://github.com/user-attachments/assets/1f66cf76-8808-4040-ad5f-2b5685c43bb1" />
---

```markdown
# BhagavadGPT

BhagavadGPT is an open-source, AI-powered spiritual guide. It uses Retrieval-Augmented Generation (RAG) combined with the lightning-fast Groq API to provide answers to modern life's questions, strictly grounded in the wisdom of the Bhagavad Gita.

## Architecture & Credits

This project is divided into three main components:

1. **The Knowledge Base (Data):** The wisdom of the Gita was manually structured into JSON files chapter by chapter. We then use a Python script (`build_db.py`) to convert these verses into vector embeddings and store them in a local **ChromaDB** database.
2. **The AI Engine (Backend):** A custom **FastAPI** Python server that takes user questions, searches the ChromaDB for the most relevant Shlokas, and feeds them to the **Groq API** (Llama 3) to generate a deeply contextual answer.
3. **The Chat Interface (Frontend):** The beautiful, locked-down chat UI is powered by **[LibreChat](https://github.com/danny-avila/LibreChat)**, a phenomenal open-source ChatGPT UI clone. We heavily customized it to use our own branding and exclusive backend endpoints.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **[Git](https://git-scm.com/downloads)** * **[Python 3.10+](https://www.python.org/downloads/)** * **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (Required for the LibreChat UI)
* **A [Groq API Key](https://console.groq.com/keys)** (Free tier)
* **Google Cloud Credentials** (Client ID and Secret for OAuth Login)

---

## Step-by-Step Installation Guide

### Step 1: Clone the Repository
Open your terminal and pull the code to your local machine:

```bash
git clone [https://github.com/himanshupdev123/BhagavadGPT.git](https://github.com/himanshupdev123/BhagavadGPT.git)
cd BhagavadGPT

```

### Step 2: Build the Vector Database

Before the AI can answer questions, we need to inject the Gita's wisdom into ChromaDB.

1. Navigate to the data folder:
```bash
cd data

```


2. Run the database builder:
```bash
python build_db.py

```



### Step 3: Set Up the AI Backend

1. Navigate to the backend folder:
```bash
cd ../bhagvadgpt-backend

```


2. Create and activate a Virtual Environment:
* **Windows:** ```bash
python -m venv venv
.\venv\Scripts\activate
```

```


* **Mac/Linux:** ```bash
python -m venv venv
source venv/bin/activate
```

```




3. Install Dependencies:
```bash
pip install -r requirements.txt

```


4. Configure Environment Variables:
Create a new file named `.env` in the `bhagvadgpt-backend` folder:
```env
GROQ_API_KEY=your_actual_groq_api_key_here

```


5. Start the Backend Server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000

```



### Step 4: Set Up the Frontend (LibreChat Vault)

Open a **new** terminal window (leave the backend running).

1. Navigate to the frontend folder:
```bash
cd BhagavadGPT/bhagvadgpt-frontend

```


2. Configure the Frontend Secrets:
Create a new file named `.env` in the `bhagvadgpt-frontend` folder:
```env
# App Branding
APP_TITLE=BhagvadGPT

# API Lock
ENDPOINTS=custom

# Security Keys
CREDS_KEY=f34be421c97eb1234567890123456789f34be421c97eb1234567890123456789
CREDS_IV=f34be421c97eb1234567890123456789
JWT_SECRET=bhagvadgpt_super_secret_jwt_key_123456789
JWT_REFRESH_SECRET=bhagvadgpt_super_secret_refresh_key_123456789

# Google OAuth Setup
ALLOW_SOCIAL_LOGIN=true
ALLOW_SOCIAL_REGISTRATION=true
DOMAIN_CLIENT=http://localhost:3080
DOMAIN_SERVER=http://localhost:3080
GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_CALLBACK_URL=/oauth/google/callback

```


3. Boot Up Docker:
Make sure Docker Desktop is running, then execute:
```bash
docker compose up -d

```



### Step 5: Access the Application! 

1. Open your web browser.
2. Go to: **`http://localhost:3080`**
3. Click "Continue with Google" to log in.
4. Begin your spiritual journey!

---

## The Team

Built with devotion by:

* Himanshu P Dev
* Hemanth
* Aashrav Sharma
* Adhya

```
