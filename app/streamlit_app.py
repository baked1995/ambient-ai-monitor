# app/streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
import os
import socket

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Ambient AI Sound Monitor",
    layout="wide"
)

st.title("🎧 Ambient AI Sound Monitor (Jetson LAN)")

# ---------------- Helper: Get Jetson IP ----------------
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
API_URL = f"http://{JETSON_IP}:8000/upload-audio"

# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs([
    "🎤 Browser Microphone",
    "📁 Upload Audio",
    "ℹ️ Info"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("Record using YOUR device microphone")

    st.info(
        "🎙 Audio is recorded directly from **your browser microphone** "
        "and saved securely on the **Jetson Orin Nano** for training."
    )

    html_path = os.path.join("app", "browser_mic.html")
    with open(html_path, "r") as f:
        html_code = f.read()

    # 🔧 Inject correct backend API URL
    html_code = html_code.replace(
        "http://localhost:8000/upload-audio",
        API_URL
    )

    components.html(html_code, height=520)

    st.caption(f"Backend API: {API_URL}")

# ================= TAB 2 =================
with tab2:
    st.subheader("Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload WAV / MP3 / FLAC file",
        type=["wav", "mp3", "flac"]
    )

    if uploaded_file:
        st.success("File uploaded successfully ✅")

        label = st.text_input(
            "Enter label for this audio",
            placeholder="e.g. keyboard, switch, harshit_voice"
        )

        if label and st.button("Save to Dataset"):
            save_dir = os.path.join("dataset", label)
            os.makedirs(save_dir, exist_ok=True)

            file_path = os.path.join(save_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success(f"Saved to `{file_path}`")

# ================= TAB 3 =================
with tab3:
    st.subheader("System Information")

    st.markdown(f"""
    ### Architecture
    - 🖥️ Backend: **Jetson Orin Nano**
    - 🌐 Access: Local network (LAN)
    - 🎙️ Audio capture: **Browser (Web Audio API)**
    - 🚀 API: **FastAPI**
    - 💾 Storage: `dataset/<label>/`

    ### Access URL
    ```
    http://{JETSON_IP}:8501
    ```

    ### API Endpoint
    ```
    http://{JETSON_IP}:8000/upload-audio
    ```

    ### Dataset Location (Jetson)
    ```
    ambient-ai-monitor/dataset/
    ```

    Designed for:
    - Speaker identification
    - Keyboard / switch classification
    - Ambient sound monitoring
    - Edge AI dataset collection
    """)
