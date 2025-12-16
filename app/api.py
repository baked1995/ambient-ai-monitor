# app/api.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import datetime

app = FastAPI(title="Ambient AI Audio API")

# Allow browser access from LAN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DATASET_DIR = "dataset"


@app.post("/upload-audio")
async def upload_audio(
    label: str = Form(...),
    file: UploadFile = Form(...)
):
    """
    Receives audio from browser mic and saves it as WAV
    """
    if not label.strip():
        return {"status": "error", "message": "Label is required"}

    # Create label directory
    label_dir = os.path.join(BASE_DATASET_DIR, label)
    os.makedirs(label_dir, exist_ok=True)

    # Create filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{label}_{timestamp}.wav"
    filepath = os.path.join(label_dir, filename)

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "label": label,
        "file": filename,
        "path": filepath
    }

