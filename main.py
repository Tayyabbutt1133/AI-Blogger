import argparse
from stt import transcribe_audio, record_audio
from prompts import get_prompt
from llm import generate_blog

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Blog Post Generator")
    parser.add_argument("--audio_path", type=str, help="Path to an existing audio file (leave empty to record live)", default=None)
    parser.add_argument("--custom_prompt", type=str, help="Custom prompt (optional)", default=None)
    args = parser.parse_args()

    # Step 1: Either record audio or use the provided file
    if args.audio_path:
        audio_path = args.audio_path  # Use existing file
    else:
        audio_path = record_audio()  # Record live audio

    # Step 2: Convert Speech to Text
    transcribed_text = transcribe_audio(audio_path)

    if not transcribed_text:
        print("Error: No text was transcribed.")
        return

    # Step 3: Get Predefined or Custom Prompt
    prompt = args.custom_prompt or get_prompt()

    # Step 4: Generate Blog Post
    blog_post = generate_blog(transcribed_text, prompt)

    # Step 5: Print Output
    print("\nGenerated Blog Post:\n")
    print(blog_post)

if __name__ == "__main__":
    main()
