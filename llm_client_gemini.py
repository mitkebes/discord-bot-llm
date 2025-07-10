# llm_client_gemini.py   
import os
import google.generativeai as genai
from typing import List, Dict

async def get_llm_response(prompt: str, system_prompt: str, history: List[Dict[str, str]] = []) -> str | None:
    """
    Sends a prompt to the Google Gemini API and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        system_prompt (str): The system prompt to set the context for the model.

    Returns:
        str | None: The text response from the model, or None if an error occurs.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return "The `GEMINI_API_KEY` is missing. Please ask the bot administrator to configure it."

    try:
        genai.configure(api_key=api_key)
        
        # In Gemini, system instructions are a specific parameter for the model
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_prompt
        )
        
        # Convert history to Gemini's format
        gemini_history = []
        for message in history:
            role = 'user' if message['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': [message['content']]})

        chat = model.start_chat(history=gemini_history)

        print("Sending request to Gemini API...")
        response = await chat.send_message_async(prompt)
        
        print("Successfully received response from Gemini API.")
        return response.text.strip()

    except Exception as e:
        print(f"An unexpected error occurred in the Gemini client: {e}")
        return f"An error occurred while contacting the Gemini API: {e}"

