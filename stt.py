import os
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from elevenlabs import ElevenLabs
import requests
import json
import traceback
from dotenv import load_dotenv
import time

# Load API key from .env file
load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

if not elevenlabs_api_key:
    raise ValueError("Error: ELEVENLABS_API_KEY is missing. Please set it in the .env file.")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=elevenlabs_api_key)

def record_audio(output_path="recorded_audio.wav", duration=50, sample_rate=44100):
    """
    Records audio from the microphone and saves it as a WAV file.

    :param output_path: Filename to save the recording.
    :param duration: Duration of recording in seconds.
    :param sample_rate: Sample rate in Hz.
    :return: Path to the saved audio file.
    """
    print(f"Recording for {duration} seconds... Speak now!")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    write(output_path, sample_rate, np.array(audio_data))  # Save as WAV file
    print(f"Audio recorded and saved as {output_path}")

    return output_path  # Return recorded file path

def transcribe_audio(audio_path, elevenlabs_api_key):
    """
    Converts speech from an audio file to text using Eleven Labs API with detailed logging.

    :param audio_path: Path to the audio file.
    :param elevenlabs_api_key: API key for Eleven Labs.
    :return: Transcribed text or None on failure.
    """
    try:
        if not elevenlabs_api_key:
            print("❌ ERROR: Eleven Labs API key is missing!")
            return None
        
        print("\n==== STARTING TRANSCRIPTION PROCESS ====")
        print(f"Audio file: {audio_path}")

        if not os.path.exists(audio_path):
            print(f"❌ ERROR: Audio file not found at {audio_path}")
            return None

        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
        print(f"📂 File size: {file_size:.2f} MB")

        url = "https://api.elevenlabs.io/v1/speech-to-text"
        print(f"🌐 Sending request to: {url}")

        headers = {"xi-api-key": elevenlabs_api_key}
        print("✅ API key configured in headers")

        # Prepare the multipart form data
        start_time = time.time()
        print("🔄 Opening audio file and preparing request...")

        with open(audio_path, "rb") as f:
            files = {"file": ("recorded_audio.wav", f, "audio/wav")}
            data = {"model_id": "scribe_v1"}

            print(f"📡 Request data: model_id={data['model_id']}")

            # Make the POST request
            print("🚀 Sending POST request to Eleven Labs API...")
            response = requests.post(url, headers=headers, files=files, data=data)

        request_time = time.time() - start_time
        print(f"✅ Request completed in {request_time:.2f} seconds")

        # Check if request was successful
        if response.status_code == 200:
            try:
                result = response.json()
                print("📜 Response JSON:", json.dumps(result, indent=2))

                transcribed_text = result.get("text", "").strip()
                if transcribed_text:
                    print(f"\n🎤 Transcription successful! Text length: {len(transcribed_text)} characters")
                    print(f"🔍 First 200 chars: \"{transcribed_text[:200]}\"...")
                    return transcribed_text
                else:
                    print("⚠️ WARNING: Response doesn't contain 'text' field")
                    return None

            except json.JSONDecodeError:
                print("❌ ERROR: Could not parse JSON response")
                print(f"📝 Raw response: {response.text[:500]}...")
                return None
        else:
            print(f"❌ ERROR: API returned status code {response.status_code}")
            print(f"⚠️ Response content: {response.text[:500]}...")
            return None

    except Exception as e:
        print(f"💥 EXCEPTION during transcription: {str(e)}")
        print(traceback.format_exc())
        return None

    finally:
        print("==== TRANSCRIPTION PROCESS COMPLETED ====\n")