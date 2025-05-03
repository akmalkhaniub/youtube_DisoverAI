from google.adk.agents import Agent
from .youtube_tools import search_youtube_videos, summarize_video


root_agent = Agent(
    name="youtube_agent",
    model="gemini-2.0-flash",
    description="Agent to search YouTube for videos based on keywords and summarize them.",
    instruction="Given a set of keywords, find relevant YouTube videos and summarize them for the user.",
    tools=[search_youtube_videos, summarize_video]
)