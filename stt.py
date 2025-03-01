import sounddevice as sd
import numpy as np
import wave
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def record_audio(filename="audio.wav", duration=30, samplerate=44100):
    """Records audio from the microphone and saves it as a WAV file."""
    print("🎙️ Recording... Speak now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    
    print("✅ Recording complete!")
    return filename


def transcribe_audio(audio_path):
    """Converts speech from an audio file to text using Eleven Labs API."""
    if not ELEVENLABS_API_KEY:
        print("❌ ERROR: Eleven Labs API key is missing!")
        return None

    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    with open(audio_path, "rb") as audio_file:
        files = {"file": ("audio.wav", audio_file, "audio/wav")}
        data = {"model_id": "scribe_v1"}
        
        print("🚀 Sending audio to Eleven Labs API for transcription...")
        start_time = time.time()
        response = requests.post(url, headers=headers, files=files, data=data)
        request_time = time.time() - start_time
    
    if response.status_code == 200:
        try:
            result = response.json()
            transcribed_text = result.get("text", "").strip()
            if transcribed_text:
                print("✅ Transcription successful!")
                print("📝 Transcribed Text:", transcribed_text)
                return transcribed_text
            else:
                print("⚠️ No transcription text found in response.")
                return None
        except json.JSONDecodeError:
            print("❌ ERROR: Failed to parse response JSON.")
            print(response.text[:500])
            return None
    else:
        print(f"❌ API returned status code {response.status_code}")
        print(response.text[:500])
        return None
