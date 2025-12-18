from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os, shutil
from datetime import datetime

app = FastAPI(title="Ambient AI Audio API")

# --------------------------------------------------
# CORS (LAN-safe; tighten later)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = "data"
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
TRAINING_DIR = os.path.join(BASE_DIR, "training")
RECOGNITION_DIR = os.path.join(BASE_DIR, "recognition")

for d in [RECORDINGS_DIR, TRAINING_DIR, RECOGNITION_DIR]:
    os.makedirs(d, exist_ok=True)

# --------------------------------------------------
# Browser Recording / Training Upload
# --------------------------------------------------
@app.post("/upload-audio")
async def upload_audio(
    speaker: str = Form(...),
    category: str = Form(...),
    file: UploadFile = Form(...)
):
    speaker = speaker.strip()
    category = category.strip()

    if not speaker or not category:
        return {"status": "error", "message": "Speaker and category required"}

    speaker_dir = os.path.join(TRAINING_DIR, speaker)
    os.makedirs(speaker_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{category}_{timestamp}.wav"
    path = os.path.join(speaker_dir, filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {
        "status": "success",
        "type": "training",
        "speaker": speaker,
        "category": category,
        "file": filename,
        "path": path
    }

# --------------------------------------------------
# Recognition-only Upload (NO training contamination)
# --------------------------------------------------
@app.post("/recognition-upload")
async def recognition_upload(
    file: UploadFile = Form(...)
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recognition_{timestamp}_{file.filename}"
    path = os.path.join(RECOGNITION_DIR, filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {
        "status": "success",
        "type": "recognition",
        "file": filename,
        "path": path
    }

# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

