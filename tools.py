from google import genai
from google.genai import types
import os
from agents import function_tool
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

@function_tool
def read_document(question: str):
    """Search the book content to answer questions about Human AI, Robotics, and Physical AI topics."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Can you tell me about {question}""",
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=["fileSearchStores/ragfilestore-tw7ieckhbt3j"]
                    )
                )
            ]
        )
    )
    return response.text