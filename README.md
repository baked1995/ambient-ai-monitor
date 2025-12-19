# 🎧 Ambient AI Sound Monitor (Jetson LAN)

An **Edge AI–based audio intelligence platform** designed for **sound recognition, speaker identification, and ambient monitoring**, optimized for **NVIDIA Jetson devices** and local LAN usage.

This system enables **browser-based audio capture**, **structured dataset creation**, and **CNN-based sound recognition** without sending audio to the cloud.

---

## 🚀 Key Capabilities

- 🎙 **Browser microphone recording** (no device mic required on Jetson)
- 📁 **Structured training data collection**
- 📤 **Recognition-only audio uploads**
- 🧠 **Pre-trained CNN-based audio recognition (YAMNet)**
- 📊 **Waveform, loudness, and spectrogram visualization**
- 🧩 **Recording profiles for high-quality dataset collection**
- 🔒 **LAN-only, privacy-preserving architecture**

---

## 🧱 System Architecture
Browser (User Device)
│
│ (Web Audio API)
▼
Streamlit UI (Jetson)
│
├── Audio Visualization
├── Recording Profiles
├── Dataset Management
│
▼
FastAPI Backend
│
├── Training Data Storage
├── Recognition Uploads
│
▼
Audio Intelligence Engine
├── YAMNet (CNN)
└── Feature Extraction

## 📂 Project Structure
ambient-ai-monitor/
├── app/
│ ├── streamlit_app.py # UI & visualization
│ ├── api.py # Audio ingestion API
│ ├── browser_mic.html # Web Audio capture
│
├── model/
│ ├── yamnet_utils.py # Model helpers (future-ready)
│
├── data/ # Runtime data (git-ignored)
│ ├── recordings/
│ ├── training/
│ └── recognition/
│
├── requirements.txt
├── .gitignore
└── README.md

> ⚠️ **Audio data is intentionally excluded from Git** to ensure privacy and clean ML workflows.

---

## 🧠 Model Lifecycle & Intelligence Pipeline

### Phase 1 — Sound Understanding (Current)

The system uses **YAMNet**, a **CNN-based audio event classifier** trained on Google’s **AudioSet** (over 2M labeled sound clips).

**Model details:**
- Architecture: **Convolutional Neural Network (CNN)**
- Input: Raw audio waveform (16 kHz mono)
- Output: Probability scores across **521 sound classes**
- Examples:
  - Human speech
  - Keyboard typing
  - Switch clicks
  - Water, wind, ambient noise

**Why YAMNet?**
- Lightweight
- Proven accuracy
- Ideal for edge devices like Jetson
- No training required initially

---

### Phase 2 — Dataset Quality & Recording Profiles (Implemented)

To ensure **high-quality training data**, the system introduces **Recording Profiles**:

| Profile | Purpose |
|------|------|
| Voice (Speaker ID) | Speaker identification datasets |
| Keyboard | Keystroke sound modeling |
| Switch / Button | Mechanical sound detection |
| Ambient Noise | Background baselining |

Each profile provides **human-readable capture guidance**, improving:
- Signal consistency
- Label accuracy
- Model performance later

---

### Phase 3 — Feature Intelligence (Implemented)

For every audio clip, the system computes:

- **RMS Energy** → loudness consistency
- **Zero Crossing Rate (ZCR)** → noise / sharpness
- **Spectral Centroid** → frequency distribution
- **Spectrogram (Log-frequency)** → time–frequency behavior

These features help:
- Detect poor recordings
- Identify noisy or silent samples
- Validate training data before ML training

---

### Phase 4 — Speaker Embeddings (Planned)

Next step will introduce **speaker embeddings**:

- Convert voice samples into **fixed-length vectors**
- Compare voices using cosine similarity
- Enable:
  - Speaker verification
  - Voice clustering
  - Unknown speaker detection

This builds on Phase 1 without retraining from scratch.

---

### Phase 5 — Custom Classifier Training (Planned)

Final phase introduces **custom ML models** trained on your collected data:

- Use YAMNet embeddings as input
- Train:
  - Speaker classifiers
  - Environment-specific sound detectors
- Models optimized for:
  - Jetson Orin Nano
  - Real-time inference
  - Offline operation

---

## 🔐 Privacy & Security

- Audio never leaves the local network
- HTTPS enforced via NGINX
- No cloud dependency
- No third-party data sharing

---

## 🧪 Ideal Use Cases

- Smart environments
- Industrial monitoring
- Healthcare ambient sensing
- Voice-based access systems
- Edge AI research & prototyping

---

## 📌 Technology Stack

- **Frontend:** Streamlit
- **Audio Capture:** Web Audio API
- **Backend:** FastAPI
- **ML Model:** YAMNet (TensorFlow Hub)
- **Visualization:** Librosa + Matplotlib
- **Deployment:** NVIDIA Jetson (Edge AI)

---

## 📈 Roadmap

- [x] Phase 1: Audio understanding
- [x] Phase 2: Recording profiles
- [x] Phase 3: Feature analytics
- [ ] Phase 4: Speaker embeddings
- [ ] Phase 5: Custom classifiers
- [ ] Phase 6: Anomaly detection

---

## 📄 License

Internal / Client-specific usage  
(Contact project owner for redistribution)
