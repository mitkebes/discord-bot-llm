# llm_client_gemini.py
import os
from google import genai
from google.genai import types
from typing import List, Dict

async def get_llm_response(prompt: str, system_prompt: str, history: List[Dict[str, str]] = [], grounding: bool = False) -> str | None:
    """
    Sends a prompt to the Google Gemini API and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        system_prompt (str): The system prompt to set the context for the model.
        history (List[Dict[str, str]]): The conversation history.
        grounding (bool): Whether to use Google Search grounding.

    Returns:
        str | None: The text response from the model, or None if an error occurs.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return "The `GEMINI_API_KEY` is missing. Please ask the bot administrator to configure it."

    # Default to gemini-2.0-flash as 1.5 might not be available in the new SDK default endpoint
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    try:
        client = genai.Client(api_key=api_key)
        
        # Convert history to Gemini's format
        gemini_history = []
        for message in history:
            role = 'user' if message['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': [{'text': message['content']}]})

        print(f"Sending request to Gemini API (Model: {model_name}, Grounding: {grounding})...")
        
        if hasattr(client, 'aio'):
            tools = []
            if grounding:
                tools.append(types.Tool(google_search=types.GoogleSearch()))

            chat = client.aio.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=tools
                ),
                history=gemini_history
            )
            response = await chat.send_message(prompt)
            
            print("Successfully received response from Gemini API.")
            return response.text.strip()
        else:
            # Fallback if aio is not available (should not happen with recent google-genai)
            print("Error: Async client not available.")
            return "Error: Async client not available."

    except Exception as e:
        print(f"An unexpected error occurred in the Gemini client: {e}")
        return f"An error occurred while contacting the Gemini API: {e}"

