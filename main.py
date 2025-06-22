# main.py
import os
import asyncio
from dotenv import load_dotenv
from bot import LLMBot

def main():
    """
    Main function to load environment variables and run the Discord bot.
    """
    load_dotenv()

    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    lm_studio_url = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")

    if not discord_token:
        print("Error: DISCORD_BOT_TOKEN not found in .env file.")
        return

    # Create an instance of the bot with a command prefix and run it
    # The command prefix is the character you'll use to issue commands, e.g., !setprompt
    client = LLMBot(command_prefix="!", lm_studio_url=lm_studio_url)
    
    try:
        client.run(discord_token)
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")

if __name__ == "__main__":
    main()

