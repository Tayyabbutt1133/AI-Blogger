import random

# Predefined prompts for structuring the blog
PREDEFINED_PROMPTS = [
    "Write an engaging and informative blog post based on the following text.",
    "Turn this into a detailed, well-structured blog post with subheadings.",
    "Summarize and format this content into a blog post with bullet points.",
    "Rewrite this as a blog with an engaging introduction and conclusion."
]

def get_prompt():
    """Let the user choose a predefined prompt or return a random one."""
    print("\nChoose a predefined prompt:")
    for idx, prompt in enumerate(PREDEFINED_PROMPTS, 1):
        print(f"{idx}. {prompt}")

    choice = input("\nEnter the number of your choice (or press Enter for random): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(PREDEFINED_PROMPTS):
        return PREDEFINED_PROMPTS[int(choice) - 1]
    
    return random.choice(PREDEFINED_PROMPTS)  # Random fallback

