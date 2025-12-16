# Ambient AI Sound Monitor (Jetson)

A browser-based, LAN-hosted audio data collection and monitoring platform
designed for NVIDIA Jetson Orin Nano.

## Features
- Browser microphone recording (Web Audio API)
- Multi-user LAN access
- Centralized dataset storage
- FastAPI backend for audio ingestion
- Streamlit UI
- Jetson-optimized deployment
- Docker support

## Architecture
Browser → FastAPI → Dataset  
Browser → Streamlit UI  

## Folder Structure
ambient-ai-monitor/
├── app/
│ ├── streamlit_app.py
│ ├── api.py
│ └── browser_mic.html
├── dataset/
├── recordings/
├── requirements.txt
├── Dockerfile.jetson


## Run Locally (Development)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
streamlit run app/streamlit_app.py




