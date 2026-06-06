import os
import time
import uuid
import wave
import asyncio
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Depends, HTTPException, status, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKeyHeader
from piper import PiperVoice
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TINYTTS_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

import tempfile
MODELS_DIR = "models"
TEMP_AUDIO_DIR = os.path.join(tempfile.gettempdir(), "tinytts_temp_audio")

MODEL_PATHS = {
    "en": {
        "female": os.path.join(MODELS_DIR, "en", "female", "en_US-hfc_female-medium.onnx"),
        "male": os.path.join(MODELS_DIR, "en", "male", "en_US-hfc_male-medium.onnx")
    },
    "hi": {
        "female": os.path.join(MODELS_DIR, "hi", "female", "hi_IN-priyamvada-medium.onnx"),
        "male": os.path.join(MODELS_DIR, "hi", "male", "hi_IN-rohan-medium.onnx")
    }
}

loaded_voices = {}
cleanup_task = None

async def cleanup_loop():
    while True:
        try:
            await asyncio.sleep(45) # Run every 10 seconds
            now = time.time()
            if os.path.exists(TEMP_AUDIO_DIR):
                for filename in os.listdir(TEMP_AUDIO_DIR):
                    if filename.endswith(".wav") or filename.endswith(".mp3"):
                        filepath = os.path.join(TEMP_AUDIO_DIR, filename)
                        # Check if file is older than 2 minutes (120 seconds)
                        if now - os.path.getmtime(filepath) > 60:
                            os.remove(filepath)
                            print(f"Deleted old audio file: {filepath}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in cleanup loop: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
    
    print("Loading models...")
    for lang, genders in MODEL_PATHS.items():
        loaded_voices[lang] = {}
        for gender, path in genders.items():
            if os.path.exists(path):
                print(f"Loading {lang}-{gender} from {path}")
                loaded_voices[lang][gender] = PiperVoice.load(path)
            else:
                print(f"Warning: Model not found at {path}")
    print("Models loaded successfully.")
    
    global cleanup_task
    cleanup_task = asyncio.create_task(cleanup_loop())
    
    yield
    
    # Shutdown
    if cleanup_task:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass

app = FastAPI(title="TinyTTS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Gender(str, Enum):
    male = "male"
    female = "female"

class Language(str, Enum):
    en = "en"
    hi = "hi"

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate_audio(
    text: str = Form(...),
    gender: Gender = Form(...),
    language: Language = Form(...),
    api_key: str = Depends(get_api_key)
):
    lang_val = language.value
    gender_val = gender.value
    
    if lang_val not in loaded_voices or gender_val not in loaded_voices[lang_val]:
        raise HTTPException(status_code=400, detail="Invalid language or gender combination")
        
    voice = loaded_voices[lang_val][gender_val]
    job_id = str(uuid.uuid4())
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{job_id}.wav")
    
    def synthesize():
        with wave.open(out_path, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
            
    # Run synchronously in a thread pool so we don't block the async event loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, synthesize)
    
    return {"job_id": job_id}

@app.post("/download")
async def download_audio(
    job_id: str = Form(...),
    api_key: str = Depends(get_api_key)
):
    # To prevent directory traversal attacks
    if not job_id.isalnum() and "-" not in job_id:
        raise HTTPException(status_code=400, detail="Invalid job_id format")
        
    file_path = os.path.join(TEMP_AUDIO_DIR, f"{job_id}.wav")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found or expired")
        
    return FileResponse(file_path, media_type="audio/wav", filename=f"{job_id}.wav")
