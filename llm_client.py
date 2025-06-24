# llm_client.py
import os
from llm_client_lmstudio import get_llm_response as get_lmstudio_response
from llm_client_gemini import get_llm_response as get_gemini_response

async def get_llm_response(prompt: str, system_prompt: str, thinking_enabled: bool = False) -> str | None:
    """
    Gets a response from the configured LLM provider.

    This function reads the `LLM_PROVIDER` environment variable to determine
    whether to use the local LM Studio server or the Google Gemini API.
    """
    provider = os.getenv("LLM_PROVIDER", "LMSTUDIO").upper()

    if provider == "GEMINI":
        print("Using Gemini API as the LLM provider.")
        # The 'thinking_enabled' flag is not applicable to Gemini, so we don't pass it.
        return await get_gemini_response(prompt, system_prompt)
    
    # For LM Studio or default, pass the thinking_enabled flag.
    elif provider == "LMSTUDIO":
        print("Using LM Studio as the LLM provider.")
        return await get_lmstudio_response(prompt, system_prompt, thinking_enabled)
    else:
        print(f"Error: Unknown LLM_PROVIDER '{provider}'. Defaulting to LMSTUDIO.")
        return await get_lmstudio_response(prompt, system_prompt, thinking_enabled)

