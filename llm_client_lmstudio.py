# llm_client_lmstudio.py
import os
import aiohttp
import json

async def get_llm_response(prompt: str, system_prompt: str) -> str | None:
    """
    Sends a prompt to the LM Studio local server and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        system_prompt (str): The system prompt to set the context for the model.

    Returns:
        str | None: The text response from the model, or None if an error occurs.
    """
    api_url = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    full_api_url = f"{api_url}/chat/completions"
    
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    print(f"Sending request to LM Studio at {full_api_url}...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_api_url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    print("Successfully received response from LM Studio.")
                    return content.strip()
                else:
                    error_text = await response.text()
                    print(f"Error from LM Studio API: Status {response.status}, Response: {error_text}")
                    return None
    except aiohttp.ClientConnectorError as e:
        print(f"Error connecting to the LM Studio server: {e}")
        return "Could not connect to the local LM Studio server. Please ensure it is running."
    except Exception as e:
        print(f"An unexpected error occurred in the LLM client: {e}")
        return None

