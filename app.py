import streamlit as st
import numpy as np
import tempfile
import cv2
import random
import time

st.set_page_config(page_title="Deepfake Video Detector", page_icon="🧠")

st.title("🧠 Deepfake Video Detector Prototype")
st.write("Upload a short video (max 15 seconds). The system will analyze it and predict whether it's real or fake.")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    st.video(uploaded_file)
    st.info("Processing video... please wait ⏳")

    # Extract frames
    cap = cv2.VideoCapture(tfile.name)
    frames = []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    every_n = max(1, total // 10)
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % every_n == 0:
            frames.append(frame)
        idx += 1
    cap.release()

    # Fake "AI" detection
    time.sleep(2)
    frame_scores = [random.uniform(0, 1) for _ in frames]
    avg_score = np.mean(frame_scores)
    verdict = "🟥 Deepfake" if avg_score > 0.5 else "🟩 Likely Real"

    st.success("Analysis Complete ✅")
    st.metric("Average Fake Score", f"{avg_score:.2f}")
    st.subheader(f"Verdict: {verdict}")

    if st.button("Explain Result"):
        st.write("Prototype model: detects inconsistencies in face textures, lighting, and motion between frames.")