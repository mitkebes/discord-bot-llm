# llm_client_lmstudio.py
import os
import aiohttp
import json
import re

async def get_llm_response(prompt: str, system_prompt: str, thinking_enabled: bool = False) -> str | None:
    """
    Sends a prompt to the LM Studio local server and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        system_prompt (str): The system prompt to set the context for the model.
        thinking_enabled (bool): If False, tries to suppress the model's thinking process.
    """
    api_url = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    full_api_url = f"{api_url}/chat/completions"
    
    prompt_to_send = prompt
    # If thinking is disabled, append the /nothink command to the user's prompt.
    if not thinking_enabled:
        prompt_to_send = f"{prompt}\n/nothink"
    
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_to_send}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    print(f"Sending request to LM Studio at {full_api_url}...")
    if thinking_enabled:
        print("Thinking mode is ENABLED.")
    else:
        print("Thinking mode is DISABLED.")


    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_api_url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    print("Successfully received response from LM Studio.")

                    final_content = content
                    # If thinking is disabled, remove <think> tags from the response.
                    if not thinking_enabled:
                        final_content = re.sub(r'</?think>', '', content).strip()

                    return final_content
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

