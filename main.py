# main.py
import os
import asyncio
from dotenv import load_dotenv
from bot import LLMBot, setup

async def main():
    """
    Main async function to load environment variables and run the Discord bot.
    
    The bot's LLM provider can be configured in the .env file.
    Set LLM_PROVIDER to "GEMINI" or "LMSTUDIO".
    - For GEMINI, add your GEMINI_API_KEY.
    - For LMSTUDIO, ensure LM_STUDIO_API_URL is set (or defaults correctly).
    """
    load_dotenv()

    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token:
        print("Error: DISCORD_BOT_TOKEN not found in .env file.")
        return

    # Bot initialization is now simpler, with no provider-specific arguments.
    client = LLMBot()

    try:
        # The setup function, imported from bot.py, adds the slash commands to the bot
        await setup(client)
        # Start the bot with the token
        await client.start(discord_token)
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")
        await client.close()

if __name__ == "__main__":
    # Use asyncio.run() to start the asynchronous main function
    asyncio.run(main())

