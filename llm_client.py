# llm_client.py
import aiohttp
import json

async def get_llm_response(prompt: str, api_url: str, system_prompt: str) -> str | None:
    """
    Sends a prompt to the LM Studio local server and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        api_url (str): The URL for the LM Studio server's chat completions endpoint.
        system_prompt (str): The system prompt to set the context for the model.

    Returns:
        str | None: The text response from the model, or None if an error occurs.
    """
    # The endpoint for LM Studio's chat completions API is typically /v1/chat/completions
    full_api_url = f"{api_url}/chat/completions"
    
    # This payload structure mimics the OpenAI API, which LM Studio uses.
    # The system prompt is now passed dynamically.
    payload = {
        "model": "local-model",  # This value doesn't matter for LM Studio
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1, # -1 for infinity
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"Sending request to LM Studio at {full_api_url} with system prompt...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_api_url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 200:
                    data = await response.json()
                    # The response structure contains the message content
                    content = data['choices'][0]['message']['content']
                    print("Successfully received response from LM Studio.")
                    return content.strip()
                else:
                    error_text = await response.text()
                    print(f"Error from LM Studio API: Status {response.status}, Response: {error_text}")
                    return None
    except aiohttp.ClientConnectorError as e:
        print(f"Error connecting to the LM Studio server: {e}")
        print("Please ensure your LM Studio server is running and the URL is correct.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in the LLM client: {e}")
        return None

