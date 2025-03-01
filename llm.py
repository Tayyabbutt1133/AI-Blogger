from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

def generate_blog(transcribed_text, prompt):
    """
    Generates a blog post using Groq LLM.

    :param transcribed_text: The transcribed text from STT.
    :param prompt: The prompt for generating the blog.
    :return: Generated blog content.
    """
    if not groq_api_key:
        return "❌ ERROR: Missing Groq API key."

    llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")

    messages = [
        SystemMessage(content="You are an AI that converts ideas into well-structured blog posts."),
        HumanMessage(content=f"Prompt: {prompt}\n\nText: {transcribed_text}")
    ]

    # Generate response
    response = llm.invoke(messages)
    
    return response.content if response else "❌ ERROR: Failed to generate blog."
