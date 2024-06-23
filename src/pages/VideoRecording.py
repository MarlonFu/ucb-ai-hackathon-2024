import uuid
from pathlib import Path

import av
import cv2
import streamlit as st
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import WebRtcMode, webrtc_streamer



def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame: # if addiitonal processing needs to be done
    img = frame.to_ndarray(format="bgr24")
    return av.VideoFrame.from_ndarray(img, format="bgr24")


RECORD_DIR = Path("./records")
RECORD_DIR.mkdir(exist_ok=True)

out_file = RECORD_DIR / f"output.mp4"

def out_recorder_factory() -> MediaRecorder:
    return MediaRecorder(str(out_file))

webrtc_streamer(
    key="record",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={
        "video": True,
        "audio": True,
    },
    out_recorder_factory=out_recorder_factory,
)

if out_file.exists():
    with out_file.open("rb") as f:
        st.download_button(
            "Download the recorded video without video filter", f, "input.mp4"
        )

        if st.button("Delete"):
            out_file.unlink()

