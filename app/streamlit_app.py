# app/streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Ambient AI Sound Monitor",
    layout="wide"
)

st.title("🎧 Ambient AI Sound Monitor (Jetson LAN)")

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
        "This records audio directly from **your browser microphone** "
        "and saves it on the Jetson Orin Nano for training."
    )

    html_path = os.path.join("app", "browser_mic.html")
    with open(html_path, "r") as f:
        html_code = f.read()

    components.html(html_code, height=360)

# ================= TAB 2 =================
with tab2:
    st.subheader("Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload WAV / MP3 / FLAC file",
        type=["wav", "mp3", "flac"]
    )

    if uploaded_file:
        st.success("File uploaded successfully ✅")
        st.write(
            "You can use this to contribute training data "
            "without recording from the browser."
        )

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

    st.markdown("""
    ### Architecture
    - App is running on **Jetson Orin Nano**
    - Hosted locally on the LAN
    - Users access via browser
    - Browser captures microphone (Web Audio API)
    - Audio sent to Jetson via FastAPI
    - Files saved in `dataset/<label>/`

    ### Access
    ```
    http://<jetson-ip>:8501
    ```

    ### Dataset Location (on Jetson)
    ```
    ambient-ai-monitor/dataset/
    ```

    This setup is designed for:
    - Speaker identification
    - Sound classification
    - Keyboard / switch / ambient noise detection
    - Edge AI data collection
    """)
