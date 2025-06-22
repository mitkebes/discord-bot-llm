# main.py
import os
import asyncio
from dotenv import load_dotenv
from bot import LLMBot, setup

async def main():
    """
    Main async function to load environment variables and run the Discord bot.
    """
    # Load environment variables from a .env file
    # This is where you'll store your Discord bot token and LM Studio URL
    load_dotenv()

    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    lm_studio_url = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1")

    if not discord_token:
        print("Error: DISCORD_BOT_TOKEN not found in .env file.")
        print("Please create a .env file and add your bot token.")
        return

    # Create an instance of the bot
    client = LLMBot(lm_studio_url=lm_studio_url)

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

