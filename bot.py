# bot.py
import discord
from llm_client import get_llm_response

class LLMBot(discord.Client):
    """
    A Discord bot that interacts with an LLM via an LM Studio server.
    """
    def __init__(self, lm_studio_url: str):
        """
        Initializes the bot with necessary intents and the LM Studio URL.

        Args:
            lm_studio_url (str): The URL of the LM Studio API endpoint.
        """
        # Define the intents required for the bot to function
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.lm_studio_url = lm_studio_url
        print("Bot initialized. Connecting to Discord...")

    async def on_ready(self):
        """
        Called when the bot has successfully connected to Discord.
        """
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print('Bot is ready to receive messages.')
        print('------')

    async def on_message(self, message: discord.Message):
        """
        Called whenever a message is sent in a channel the bot has access to.

        Args:
            message (discord.Message): The message object from Discord.
        """
        # 1. Ignore messages sent by the bot itself to prevent loops
        if message.author == self.user:
            return

        # 2. Check if the bot was mentioned in the message
        if self.user.mentioned_in(message):
            # Use typing indicator to show the bot is "thinking"
            async with message.channel.typing():
                try:
                    # Clean the message content to get the user's prompt
                    # This removes the bot's mention from the text
                    prompt = message.content.replace(f'<@!{self.user.id}>', '').strip()
                    
                    if not prompt:
                        await message.channel.send("You mentioned me, but didn't ask anything! How can I help?")
                        return

                    print(f"Received prompt from {message.author.name}: '{prompt}'")

                    # 3. Get the response from the LM Studio server
                    llm_response = await get_llm_response(prompt, self.lm_studio_url)

                    # 4. Send the response back to the Discord channel
                    if llm_response:
                        # Discord has a 2000 character limit per message
                        if len(llm_response) > 2000:
                            await message.channel.send("The response is too long! Here's the first part:")
                            await message.channel.send(llm_response[:2000])
                        else:
                            await message.channel.send(llm_response)
                    else:
                        await message.channel.send("Sorry, I couldn't get a response from the model. Please check if the LM Studio server is running correctly.")

                except Exception as e:
                    print(f"An error occurred while processing a message: {e}")
                    await message.channel.send("An unexpected error occurred. Please check the bot's console for details.")

