import streamlit as st
import tempfile
import os
import sounddevice as sd
import wave
from stt import transcribe_audio
from llm import generate_blog

# Streamlit UI
st.title("🎙️ AI-Powered Voice-to-Blog Generator")
st.write("Record or upload an audio file, and AI will generate a blog post for you.")

st.sidebar.header("🔑 API Key Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("Enter Eleven Labs API Key", type="password")

# Lock everything until both API keys are provided
if not groq_api_key.strip() or not elevenlabs_api_key.strip():
    st.warning("⚠️ Please enter both API keys to proceed.")
    st.stop()  # Stop execution until API keys are entered

st.sidebar.header("📝 Blog Prompt")
custom_prompt = st.sidebar.text_area(
    "Enter Your Prompt *️⃣", 
    value="", 
    help="Describe the blog topic (e.g., 'Write about the impact of AI in healthcare.')"
)

# Lock everything until a prompt is provided
if not custom_prompt.strip():
    st.warning("⚠️ Please enter a prompt to continue.")
    st.stop()  # Stop execution until a prompt is provided

# Function to record audio
def record_audio(duration=30, samplerate=44100):
    """Record audio and save as a temporary WAV file."""
    st.write("🎤 Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Save as temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        return temp_file.name  # Return file path

# Audio Upload & Recording Section
st.subheader("🎙️ Record or Upload Audio")
audio_file = st.file_uploader("Upload an audio file", type=["wav"])

if st.button("🔴 Record Audio"):
    audio_file = record_audio()

if audio_file:
    st.audio(audio_file, format="audio/wav")

    # Convert Speech to Text
    st.subheader("🔠 Transcribing Audio...")
    transcribed_text = transcribe_audio(audio_file, elevenlabs_api_key)

    if transcribed_text:
        st.success("✅ Transcription Successful!")
        
        # Generate Blog Post
        st.subheader("✍️ Generating Blog Post...")
        blog_post = generate_blog(transcribed_text, custom_prompt, groq_api_key)
        st.text_area("Generated Blog Post:", blog_post, height=300)
    else:
        st.error("❌ No text was transcribed. Please check the audio quality.")

st.caption("Powered by Generative AI 🚀")
