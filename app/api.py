# app/api.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from datetime import datetime

# --------------------------------------------------
# App initialization
# --------------------------------------------------
app = FastAPI(title="Ambient AI Audio API")

# Allow browser access from LAN / Streamlit iframe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # OK for LAN, tighten later if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Dataset configuration
# --------------------------------------------------
BASE_DATASET_DIR = "dataset"
os.makedirs(BASE_DATASET_DIR, exist_ok=True)

# --------------------------------------------------
# Upload endpoint (Browser Mic)
# --------------------------------------------------
@app.post("/upload-audio")
async def upload_audio(
    label: str = Form(...),
    file: UploadFile = Form(...)
):
    """
    Receives audio from browser microphone (MediaRecorder)
    and saves it as a WAV file under dataset/<label>/
    """

    # Validate label
    label = label.strip()
    if not label:
        return {
            "status": "error",
            "message": "Label is required"
        }

    # Create label directory
    label_dir = os.path.join(BASE_DATASET_DIR, label)
    os.makedirs(label_dir, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{label}_{timestamp}.wav"
    filepath = os.path.join(label_dir, filename)

    # Save uploaded audio
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "message": "Audio saved successfully",
        "label": label,
        "filename": filename,
        "path": filepath
    }

# --------------------------------------------------
# Health check (optional but useful)
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

