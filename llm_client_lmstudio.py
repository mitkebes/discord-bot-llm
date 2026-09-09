# llm_client_lmstudio.py
import os
import aiohttp
import json
import re
from typing import List, Dict, Optional


async def get_llm_response(
    prompt: str,
    system_prompt: str,
    thinking_enabled: bool = False,
    history: Optional[List[Dict[str, str]]] = None,
    model_name: Optional[str] = None
) -> Optional[str]:
    """
    Sends a prompt to the LM Studio local server and gets a response.

    Args:
        prompt (str): The user's prompt to send to the language model.
        system_prompt (str): The system prompt to set the context for the model.
        thinking_enabled (bool): If False, tries to suppress the model's thinking process.
        history (List[Dict[str, str]]): The conversation history.
        model_name (str): The model name for LM Studio (defaults to 'local-model').

    Returns:
        Optional[str]: Text response or detailed error message.
    """
    if history is None:
        history = []

    api_url = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")
    full_api_url = f"{api_url}/chat/completions"
    
    prompt_to_send = prompt
    # If thinking is disabled, append the /nothink command to the user's prompt.
    if not thinking_enabled:
        prompt_to_send = f"{prompt}\n/nothink"

    messages = [
        {"role": "system", "content": system_prompt}
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt_to_send})
    
    payload = {
        "model": model_name or "local-model",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    print(f"Sending request to LM Studio at {full_api_url} (Model: {payload['model']})...")
    if thinking_enabled:
        print("Thinking mode is ENABLED.")
    else:
        print("Thinking mode is DISABLED.")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(full_api_url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 200:
                    data = await response.json()
                    choices = data.get('choices', [])
                    if choices and 'message' in choices[0] and 'content' in choices[0]['message']:
                        content = choices[0]['message']['content']
                        print("Successfully received response from LM Studio.")

                        final_content = content
                        if not thinking_enabled:
                            final_content = re.sub(r'</?think>', '', content).strip()

                        return final_content
                    else:
                        return "⚠️ **LM Studio Error**: Received unexpected response format with no content choices."
                else:
                    error_text = await response.text()
                    print(f"Error from LM Studio API: Status {response.status}, Response: {error_text}")
                    return f"⚠️ **LM Studio Error (HTTP {response.status})**: {error_text}"
    except aiohttp.ClientConnectorError as e:
        print(f"Error connecting to the LM Studio server: {e}")
        return f"⚠️ **LM Studio Connection Error**: Could not connect to local LM Studio server at `{full_api_url}`. Please ensure LM Studio is running with its local server started."
    except Exception as e:
        print(f"An unexpected error occurred in the LM Studio client: {e}")
        return f"⚠️ **LM Studio Error**: {e}"
