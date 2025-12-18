import streamlit as st
import streamlit.components.v1 as components
import os
import socket
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
import requests

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Ambient AI Sound Monitor", layout="wide")
st.title("🎧 Ambient AI Sound Monitor (Jetson LAN)")

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DATA = "data"
RECORDINGS_DIR = os.path.join(BASE_DATA, "recordings")
TRAINING_DIR = os.path.join(BASE_DATA, "training")
RECOGNITION_DIR = os.path.join(BASE_DATA, "recognition")

for d in [RECORDINGS_DIR, TRAINING_DIR, RECOGNITION_DIR]:
    os.makedirs(d, exist_ok=True)

# --------------------------------------------------
# Network Helpers
# --------------------------------------------------
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "localhost"
    finally:
        s.close()
    return ip

JETSON_IP = get_local_ip()
API_BASE = f"https://{JETSON_IP}/api"

# --------------------------------------------------
# Recording Profiles (Phase 2 – capture only)
# --------------------------------------------------
RECORDING_PROFILES = {
    "Voice (Speaker ID)": "Speak clearly at normal volume. Avoid background noise.",
    "Keyboard": "Press keys naturally. Avoid touching the mic.",
    "Switch / Button": "Toggle the switch clearly multiple times.",
    "Ambient Noise": "Do not speak. Capture room background noise."
}

# --------------------------------------------------
# Load YAMNet
# --------------------------------------------------
@st.cache_resource
def load_yamnet():
    model = hub.load("https://tfhub.dev/google/yamnet/1")
    class_map = tf.keras.utils.get_file(
        "yamnet_class_map.csv",
        "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv"
    )
    classes = [l.split(",")[2] for l in open(class_map).read().splitlines()[1:]]
    return model, classes

yamnet, yamnet_classes = load_yamnet()

def run_yamnet(audio):
    audio = audio.astype(np.float32)
    scores, _, _ = yamnet(audio)
    mean_scores = tf.reduce_mean(scores, axis=0)
    top = tf.argsort(mean_scores, direction="DESCENDING")[:5]
    return [(yamnet_classes[int(i)], float(mean_scores[i])) for i in top]

# --------------------------------------------------
# Visualizations
# --------------------------------------------------
def plot_waveform(audio, sr):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(np.linspace(0, len(audio) / sr, len(audio)), audio)
    ax.set_title("Waveform")
    st.pyplot(fig)

def plot_db(audio, sr):
    rms = librosa.feature.rms(y=audio)[0]
    times = librosa.times_like(rms, sr=sr)
    db = librosa.amplitude_to_db(rms, ref=np.max)
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(times, db)
    ax.set_title("Loudness (dB)")
    st.pyplot(fig)

def plot_spectrogram(audio, sr):
    fig, ax = plt.subplots(figsize=(10, 4))
    S = librosa.stft(audio, n_fft=1024, hop_length=256)
    S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    librosa.display.specshow(
        S_db, sr=sr, hop_length=256,
        x_axis="time", y_axis="log", ax=ax
    )
    ax.set_title("Spectrogram")
    st.pyplot(fig)

# --------------------------------------------------
# ✅ Feature Metrics (RESTORED – Phase 1)
# --------------------------------------------------
def compute_audio_metrics(audio, sr):
    return {
        "RMS": float(np.mean(librosa.feature.rms(y=audio))),
        "Zero Crossing Rate": float(np.mean(librosa.feature.zero_crossing_rate(audio))),
        "Spectral Centroid (Hz)": float(np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))),
        "Duration (s)": len(audio) / sr
    }

def show_quality_warnings(metrics):
    warnings = []

    if metrics["Duration (s)"] < 1.0:
        warnings.append("⚠️ Audio too short (<1s)")

    if metrics["RMS"] < 0.01:
        warnings.append("⚠️ Audio very quiet / near silence")

    if metrics["Zero Crossing Rate"] > 0.3:
        warnings.append("⚠️ High noise or unstable signal")

    if metrics["Spectral Centroid (Hz)"] < 500:
        warnings.append("⚠️ Dominated by low frequencies")

    if warnings:
        st.warning("Recording Quality Warnings")
        for w in warnings:
            st.write(w)

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙 Browser Recording",
    "📁 Training Upload",
    "📤 Recognition Upload",
    "🧠 Audio Recognition",
    "ℹ️ Info"
])

# ==================================================
# TAB 1 — Browser Recording
# ==================================================
with tab1:
    profile = st.selectbox("Recording Profile", RECORDING_PROFILES.keys())
    st.info(RECORDING_PROFILES[profile])

    html_path = os.path.join("app", "browser_mic.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            html = f.read()
        html = html.replace(
            "http://localhost:8000/upload-audio",
            f"{API_BASE}/upload-audio"
        )
        components.html(html, height=560)

# ==================================================
# TAB 2 — Training Upload
# ==================================================
with tab2:
    profile = st.selectbox("Recording Profile", RECORDING_PROFILES.keys(), key="train_profile")
    st.info(RECORDING_PROFILES[profile])

    file = st.file_uploader("Training audio", type=["wav", "mp3", "flac"])
    speaker = st.text_input("Speaker ID")
    category = st.text_input("Category")

    if file and speaker and category and st.button("Upload Training Audio"):
        requests.post(
            f"{API_BASE}/upload-audio",
            files={"file": file},
            data={"speaker": speaker, "category": category},
            verify=False
        )
        st.success("Training audio uploaded")

# ==================================================
# TAB 3 — Recognition Upload
# ==================================================
with tab3:
    file = st.file_uploader("Recognition audio", type=["wav", "mp3", "flac"])
    if file and st.button("Upload for Recognition"):
        requests.post(
            f"{API_BASE}/recognition-upload",
            files={"file": file},
            verify=False
        )
        st.success("Recognition audio uploaded")

# ==================================================
# TAB 4 — Audio Recognition (ANALYSIS ONLY)
# ==================================================
with tab4:
    files = os.listdir(RECOGNITION_DIR)
    if not files:
        st.warning("No recognition audio available")
    else:
        selected = st.selectbox("Select audio", files)
        duration = st.slider("Analyze duration (seconds)", 1, 15, 5)

        if st.button("Run Recognition"):
            path = os.path.join(RECOGNITION_DIR, selected)
            audio, sr = librosa.load(path, sr=16000)
            audio = audio[: duration * sr]

            # 🔍 Metrics panel (RESTORED)
            metrics = compute_audio_metrics(audio, sr)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("RMS", f"{metrics['RMS']:.4f}")
            col2.metric("ZCR", f"{metrics['Zero Crossing Rate']:.4f}")
            col3.metric("Centroid (Hz)", f"{metrics['Spectral Centroid (Hz)']:.1f}")
            col4.metric("Duration (s)", f"{metrics['Duration (s)']:.2f}")

            show_quality_warnings(metrics)

            plot_waveform(audio, sr)
            plot_db(audio, sr)
            plot_spectrogram(audio, sr)

            st.markdown("### Detected Sounds")
            for label, score in run_yamnet(audio):
                st.write(f"**{label}** — {score:.2%}")

# ==================================================
# TAB 5 — Info
# ==================================================
with tab5:
    st.markdown("""
### Stable Architecture
- Recording profiles guide **data collection**
- Recognition remains **profile-agnostic**
- Clean separation of training vs inference
- Phase 1 + Phase 2 fully preserved
""")
