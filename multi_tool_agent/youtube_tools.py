import os
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
USE_VERTEX = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"

# Configure genai for either Vertex AI (ADC) or public API key
if not USE_VERTEX:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    # For Vertex, rely on ADC (gcloud auth or service account); do not set api_key
    genai.configure()

from google.adk.agents import Agent

def search_youtube_videos(keywords: str, max_results: int = 5) -> list:
    """Searches YouTube for videos matching the keywords and returns a list of video details."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=keywords,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        videos.append({
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"]
        })
    return videos

def summarize_video(details: dict) -> str:
    """Summarizes a YouTube video using Gemini, given its details (title, description)."""
    model_name = "gemini-2.5-flash-preview-04-17"
    model = genai.GenerativeModel(model_name)
    prompt = f"""
    Summarize the following YouTube video for a user who wants a quick overview:
    Title: {details['title']}
    Description: {details['description']}
    """
    summary = model.generate_content(prompt)
    return summary.text if hasattr(summary, "text") else str(summary)

