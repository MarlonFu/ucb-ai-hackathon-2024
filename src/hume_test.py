import requests
#from dotenv import load_dotenv
from hume import HumeBatchClient
from hume.models.config import FaceConfig
import io
import os
os.environ['HUME_API_KEY'] = 'VkauzES6w6sgkp8Hy1N62pAJLGbgF8kmUXAOE6RFryg4XOfA'
API_KEY = os.environ['HUME_API_KEY']


import streamlit as st
from st_audiorec import st_audiorec

def analyze_expression(file):
    job_start_response = requests.post(
        "https://api.hume.ai/v0/batch/jobs",
        headers={
            "X-Hume-Api-Key": API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "file": [('TEST.wav', file)]
        },
    )
    #print(job_start_response)
    job_id = job_start_response.json()['job_id']

    job_status = None
    while job_status != 'COMPLETED':
        job_status_response = requests.get(
            "https://api.hume.ai/v0/batch/jobs/{job_id}".format(job_id=job_id),
            headers={
                "X-Hume-Api-Key": API_KEY
            },
        )
        job_status = job_status_response.json()['state']['status']
        
    predictions_response = requests.get(
        "https://api.hume.ai/v0/batch/jobs/{job_id}/predictions".format(job_id=job_id),
        headers={
            "X-Hume-Api-Key": API_KEY
        },
    )
    #print(len(predictions_response.json()))
    return predictions_response.json()['results']['predictions']


st.title("Audio Recorder")
st.write("What do you like about this job posting?")
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')
    # Convert the wav_audio_data to a file-like object
    wav_audio_file = io.BytesIO(wav_audio_data)

    # Optionally save the file-like object as an actual file
    with open('output.wav', 'wb') as f:
        f.write(wav_audio_file.getbuffer())

    # Read the saved file in binary mode
    with open('output.wav', 'rb') as file:
        file_data = file.read()
    
    st.write(analyze_expression(file_data))



