# bot.py
import discord
from discord import app_commands
from discord.ext import commands
from llm_client import get_llm_response
import json
from typing import List

class LLMBot(commands.Bot):
    """
    A Discord bot that uses slash commands to interact with an LLM.
    """
    def __init__(self, lm_studio_url: str):
        """
        Initializes the bot. We pass a dummy command_prefix because it's required,
        but we'll be using slash commands.
        """
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        # The prefix is required for commands.Bot but won't be used for slash commands.
        super().__init__(command_prefix="!", intents=intents)

        self.lm_studio_url = lm_studio_url
        self.prompts = self.load_prompts()
        self.system_prompt = self.prompts.get("default", "You are a helpful assistant.")
        print("Bot initialized. Connecting to Discord...")

    def load_prompts(self) -> dict:
        """Loads system prompts from the prompts.json file."""
        try:
            with open("prompts.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: prompts.json not found. Using default prompt only.")
            return {"default": "You are a helpful assistant."}
        except json.JSONDecodeError:
            print("Error: Could not decode prompts.json. Please check its format.")
            return {"default": "You are a helpful assistant."}

    async def setup_hook(self):
        """
        This is called automatically when the bot logs in.
        It's the perfect place to sync our slash commands with Discord.
        """
        await self.tree.sync()
        print("Slash commands have been synced.")

    async def on_ready(self):
        """Called when the bot has successfully connected to Discord."""
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print('Bot is ready to receive commands and messages.')
        print('------')

    async def on_message(self, message: discord.Message):
        """Called whenever a message is sent."""
        if message.author == self.user:
            return

        # We no longer need to process text commands.
        # This part now only handles direct mentions of the bot.
        if self.user.mentioned_in(message):
            async with message.channel.typing():
                try:
                    # Clean the prompt to remove the bot mention
                    prompt = message.content.replace(f'<@!{self.user.id}>', '').replace(f'<@{self.user.id}>', '').strip()
                    
                    if not prompt:
                        await message.channel.send("You mentioned me, but didn't ask anything! How can I help?")
                        return

                    print(f"Received prompt from {message.author.name}: '{prompt}'")
                    llm_response = await get_llm_response(prompt, self.lm_studio_url, self.system_prompt)

                    if llm_response:
                        if len(llm_response) > 2000:
                            parts = [llm_response[i:i+2000] for i in range(0, len(llm_response), 2000)]
                            for part in parts:
                                await message.channel.send(part)
                        else:
                            await message.channel.send(llm_response)
                    else:
                        await message.channel.send("Sorry, I couldn't get a response from the model.")
                
                except Exception as e:
                    print(f"An error occurred while processing a message: {e}")
                    await message.channel.send("An unexpected error occurred.")

# --- Slash Commands ---

# The `setprompt` command with autocomplete for the `name` argument.
@app_commands.command(name="setprompt", description="Sets the system prompt for the bot.")
@app_commands.describe(name="Choose a preset or type your own custom prompt.")
async def setprompt(interaction: discord.Interaction, name: str):
    bot = interaction.client
    if name in bot.prompts:
        bot.system_prompt = bot.prompts[name]
        await interaction.response.send_message(f"System prompt changed to **{name}**.", ephemeral=True)
    else:
        bot.system_prompt = name
        await interaction.response.send_message(f"Custom system prompt has been set.", ephemeral=True)

@setprompt.autocomplete('name')
async def setprompt_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    bot = interaction.client
    # Filter prompts based on user's current input
    choices = [
        app_commands.Choice(name=prompt_name, value=prompt_name)
        for prompt_name in bot.prompts if current.lower() in prompt_name.lower()
    ]
    # Return up to 25 choices, as per Discord's limit
    return choices[:25]

@app_commands.command(name="prompt", description="Shows the current system prompt.")
async def prompt(interaction: discord.Interaction):
    bot = interaction.client
    await interaction.response.send_message(f"**Current System Prompt:**\n```\n{bot.system_prompt}\n```", ephemeral=True)

@app_commands.command(name="prompts", description="Lists all available preset prompts.")
async def list_prompts(interaction: discord.Interaction):
    bot = interaction.client
    if not bot.prompts:
        await interaction.response.send_message("No predefined prompts found.", ephemeral=True)
        return

    embed = discord.Embed(title="Available System Prompts", color=discord.Color.blue())
    for name, content in bot.prompts.items():
        # Show the first 100 characters of the prompt
        embed.add_field(name=name, value=f"```{content[:100]}...```", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@app_commands.command(name="help", description="Shows the list of available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", description="Here are the available slash commands:", color=discord.Color.green())
    embed.add_field(name="/setprompt [name|custom]", value="Sets the bot's system prompt. Use a preset name or type your own.", inline=False)
    embed.add_field(name="/prompt", value="Displays the current system prompt.", inline=False)
    embed.add_field(name="/prompts", value="Lists all available preset prompts.", inline=False)
    embed.add_field(name="/help", value="Shows this help message.", inline=False)
    embed.add_field(name="Mention the bot (@BotName)", value="Ask the bot a question directly by mentioning it.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# We need to add the commands to the bot's command tree
async def setup(bot: commands.Bot):
    bot.tree.add_command(setprompt)
    bot.tree.add_command(prompt)
    bot.tree.add_command(list_prompts)
    bot.tree.add_command(help_command)

