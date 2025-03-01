import streamlit as st
from audio_recorder_streamlit import audio_recorder
import requests
import json
import time
import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def transcribe_audio(audio_bytes, elevenlabs_api_key):
    """
    Converts speech from an audio file to text using Eleven Labs API.

    :param audio_bytes: Audio file bytes.
    :param elevenlabs_api_key: API key for Eleven Labs.
    :return: Transcribed text or None on failure.
    """
    if not elevenlabs_api_key:
        st.error("❌ ERROR: Eleven Labs API key is missing!")
        return None

    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": elevenlabs_api_key}

    st.write("🚀 Sending audio to Eleven Labs API for transcription...")

    files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
    data = {"model_id": "scribe_v1"}

    start_time = time.time()
    response = requests.post(url, headers=headers, files=files, data=data)
    request_time = time.time() - start_time

    if response.status_code == 200:
        try:
            result = response.json()
            transcribed_text = result.get("text", "").strip()
            if transcribed_text:
                st.success("✅ Transcription successful!")
                st.write(transcribed_text)
                return transcribed_text
            else:
                st.warning("⚠️ No transcription text found in response.")
                return None
        except json.JSONDecodeError:
            st.error("❌ ERROR: Failed to parse response JSON.")
            st.text(response.text[:500])
            return None
    else:
        st.error(f"❌ API returned status code {response.status_code}")
        st.text(response.text[:500])
        return None


# Streamlit App UI
st.title("🎙️ Speech-to-Text Transcription with Eleven Labs")

# Record audio using `audio_recorder_streamlit`
audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    # Transcribe audio if API key is set
    if ELEVENLABS_API_KEY:
        transcribe_audio(audio_bytes, ELEVENLABS_API_KEY)
    else:
        st.error("❌ Missing Eleven Labs API Key! Please check your .env file.")

# Option to upload an existing audio file
st.write("📂 Or upload an existing WAV file for transcription:")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    transcribe_audio(uploaded_file, ELEVENLABS_API_KEY)
