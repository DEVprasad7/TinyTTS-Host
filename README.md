<div align="center">
  <h1>🗣️ TinyTTS-Host</h1>
  <p><strong>A lightweight, fast, and secure Text-to-Speech (TTS) application powered by piper-tts.</strong></p>

  <!-- Badges -->
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img alt="Piper TTS" src="https://img.shields.io/badge/Piper_TTS-Synthesizer-8A2BE2?style=for-the-badge" />
  </p>
  <p>
    <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
    <img alt="CSS3" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
    <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  </p>
  <p>
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />
    <img alt="Status: Active" src="https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge" />
  </p>
</div>

<br />

The project features a **FastAPI** backend that handles local inference and a standalone, beautifully styled **Neo-Brutalist frontend**.

---

## 📂 Project Structure

The project is distinctly divided into two decoupled components:

```text
TinyTTS-API/
├── backend/                  # ⚙️ FastAPI backend server
│   ├── app.py                # Core API endpoints & logic
│   ├── run.py                # Uvicorn entry point
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Backend environment variables
│   ├── models/               # Downloaded ONNX voice models (en, hi)
│   └── venv/                 # Virtual environment
└── frontend/                 # 🎨 Static HTML/CSS/JS Neo-Brutalist Web App
    ├── index.html            # Main UI
    ├── style.css             # Theme & styling
    └── script.js             # API integration logic
```

---

## 🛠️ Backend Setup & Installation

Follow these steps to securely set up and run the local backend server.

### 1. Create a Virtual Environment
Navigate to the `backend` folder and isolate your dependencies by creating a new Python virtual environment:
```bash
cd backend
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Requirements
With the virtual environment activated, install the required packages (FastAPI, Uvicorn, Piper, etc.):
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Create a `.env` file inside the `backend` directory and define your secret API key to protect your server:
```env
TINYTTS_API_KEY=your_super_secret_key_here
```
*(Psst! If you just want the default API key for local testing, scroll to the very bottom of this README to find the hidden copy button!)*

### 5. Running the Server
Start the FastAPI server. **(Note: We run without hot-reloading to prevent Uvicorn from abruptly restarting when it detects new temporary audio files being created).**
```bash
python run.py
```
The server will now be listening on `http://127.0.0.1:8000`.

---

## 🚀 Frontend Setup & Usage

The frontend is a vanilla static web app. No NodeJS, NPM, or complex bundlers are required. It embraces the Neo-Brutalist web design trend.

### Local Development
1. Open `frontend/index.html` directly in your browser, or use a simple static server (e.g., `python -m http.server 8080`).
2. Type the identical API key you configured in the backend `.env` file into the **API Key** input box on the webpage.
3. Select your language, type your text, and generate your audio!

### 🌐 Production / GitHub Pages Redirects Guide
If you deploy the frontend to GitHub Pages (`username.github.io`), you must configure it to point to your live backend server:
1. Open `frontend/script.js`.
2. Change the `API_BASE_URL` at the top of the file from `http://127.0.0.1:8000` to your deployed backend's URL (e.g., `https://api.yourdomain.com`).
3. **Note:** Since this is a simple static site without client-side routing, you do not need complex SPA redirect rules (like `_redirects` or `404.html` hacks) for GitHub Pages. Just push the folder, enable GitHub pages on the `main` branch, and it will work instantly!

---

## 📡 API Endpoints Guide

The backend exposes the following endpoints. 

> **⚠️ Security Requirement:** All `POST` endpoints require the `X-API-Key` header for authorization.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Root check. Returns `{"status": "ok"}`. |
| `/health` | `GET` | Health check endpoint to verify the server is active. |
| `/generate` | `POST` | Accepts `text`, `language`, and `gender` via `multipart/form-data`. Synthesizes audio using Piper and returns a `job_id`. |
| `/download` | `POST` | Accepts `job_id` via `multipart/form-data`. Returns the synthesized `.wav` file as a binary Blob. |

---

<div align="center">
  <i>Built with ❤️ for rapid, local TTS.</i>
</div>

<br><br><br><br>

<div align="center">
  <details>
    <summary>🕵️‍♂️ You found it! Click here to reveal the default API Key</summary>
    <br>
    <p>Use the copy button on the code block below to grab the key for the frontend!</p>

```text
tinytts-1ucF3t9cH9ll0w01lD
```

  </details>
</div>