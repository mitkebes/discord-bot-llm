# bot.py
import discord
from discord import app_commands
from discord.ext import commands
from llm_client import get_llm_response
import json
from typing import List
import random
import re

class LLMBot(commands.Bot):
    """
    A Discord bot that uses slash commands to interact with a configured LLM.
    """
    def __init__(self):
        """
        Initializes the bot. The LLM provider is configured via environment variables.
        """
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        # The prefix is required but won't be used for slash commands.
        super().__init__(command_prefix="!", intents=intents)

        self.prompts = self.load_prompts()
        self.banned_words = self.load_banned_words() # Load banned words
        self.system_prompt = self.prompts.get("default", "You are a helpful assistant.")
        # Attributes for random and thinking modes
        self.random_mode = False
        self.last_random_prompt = None
        self.thinking_enabled = False
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

    def load_banned_words(self) -> List[str]:
        """Loads banned words from the banned_words.json file."""
        try:
            with open("banned_words.json", "r") as f:
                words = json.load(f)
                # Ensure all words are lowercase for case-insensitive matching
                return [word.lower() for word in words]
        except FileNotFoundError:
            print("Warning: banned_words.json not found. No words will be banned.")
            return []
        except json.JSONDecodeError:
            print("Error: Could not decode banned_words.json. No words will be banned.")
            return []

    def contains_banned_word(self, text: str) -> bool:
        """Checks if the given text contains any banned words (case-insensitive)."""
        if not self.banned_words:
            return False
        # Use regex to check for whole words to avoid partial matches (e.g., 'assist' in 'assistant')
        for word in self.banned_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text.lower()):
                return True
        return False

    async def setup_hook(self):
        """Syncs slash commands when the bot logs in."""
        await self.tree.sync()
        print("Slash commands have been synced.")

    async def on_ready(self):
        """Called when the bot has successfully connected to Discord."""
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print('Bot is ready to receive commands and messages.')
        print('------')

    async def on_message(self, message: discord.Message):
        """Handles direct mentions to the bot."""
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            async with message.channel.typing():
                try:
                    prompt = message.content.replace(f'<@!{self.user.id}>', '').replace(f'<@{self.user.id}>', '').strip()
                    
                    if not prompt:
                        await message.channel.send("You mentioned me, but didn't ask anything! How can I help?")
                        return
                    
                    # Check user's prompt for banned words
                    if self.contains_banned_word(prompt):
                        await message.channel.send("I'm sorry, but your message contains inappropriate language and cannot be processed.")
                        print(f"Rejected prompt from {message.author.name} due to banned word.")
                        return

                    print(f"Received prompt from {message.author.name}: '{prompt}'")
                    
                    current_system_prompt = self.system_prompt
                    if self.random_mode:
                        available_prompts = list(self.prompts.values())
                        if available_prompts:
                            chosen_prompt = random.choice(available_prompts)
                            self.last_random_prompt = chosen_prompt
                            current_system_prompt = chosen_prompt
                            print(f"Random mode ON. Using prompt: {chosen_prompt[:60]}...")
                        else:
                            print("Random mode ON, but no prompts are available. Using default.")

                    llm_response = await get_llm_response(prompt, current_system_prompt, self.thinking_enabled)

                    if llm_response:
                        # Check AI's response for banned words
                        if self.contains_banned_word(llm_response):
                            await message.channel.send("I'm sorry, the generated response contained inappropriate content and has been blocked.")
                            print("Blocked an AI response due to a banned word.")
                            return

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
# (The rest of the slash commands remain the same)

@app_commands.command(name="setprompt", description="Sets the system prompt for the bot. This disables random mode.")
@app_commands.describe(name="Choose a preset or type your own custom prompt.")
async def setprompt(interaction: discord.Interaction, name: str):
    bot = interaction.client
    
    response_parts = []
    if bot.random_mode:
        bot.random_mode = False
        response_parts.append("🎲 Random prompt mode has been **disabled**.")

    if name in bot.prompts:
        bot.system_prompt = bot.prompts[name]
        response_parts.append(f"System prompt changed to **{name}**.")
    else:
        bot.system_prompt = name
        response_parts.append(f"Custom system prompt has been set.")
    
    await interaction.response.send_message("\n".join(response_parts), ephemeral=True)


@setprompt.autocomplete('name')
async def setprompt_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    bot = interaction.client
    choices = [
        app_commands.Choice(name=prompt_name, value=prompt_name)
        for prompt_name in bot.prompts if current.lower() in prompt_name.lower()
    ]
    return choices[:25]

@app_commands.command(name="prompt", description="Shows the current system prompt or random mode status.")
async def prompt(interaction: discord.Interaction):
    bot = interaction.client
    if bot.random_mode:
        response_message = "🎲 **Random prompt mode is ON.**"
        if bot.last_random_prompt:
            response_message += f"\n\n**Last Used Prompt:**\n```\n{bot.last_random_prompt}\n```"
        else:
            response_message += "\n\nA random prompt will be picked for the next message you send me."
        await interaction.response.send_message(response_message, ephemeral=True)
    else:
        await interaction.response.send_message(f"**Current System Prompt:**\n```\n{bot.system_prompt}\n```", ephemeral=True)

@app_commands.command(name="random", description="Toggle random system prompts for each reply.")
@app_commands.describe(enabled="Set to 'True' to enable, 'False' to disable.")
async def random_command(interaction: discord.Interaction, enabled: bool):
    bot = interaction.client
    bot.random_mode = enabled
    if enabled:
        bot.last_random_prompt = None
        await interaction.response.send_message("✅ Random prompt mode has been **enabled**.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Random prompt mode has been **disabled**.", ephemeral=True)

@app_commands.command(name="think", description="Toggle whether the bot shows its thought process (LM Studio only).")
@app_commands.describe(enabled="Set to 'True' to enable, 'False' to disable.")
async def think_command(interaction: discord.Interaction, enabled: bool):
    bot = interaction.client
    bot.thinking_enabled = enabled
    if enabled:
        await interaction.response.send_message("🤔 Thinking mode has been **enabled**. The bot will now show its thought process.", ephemeral=True)
    else:
        await interaction.response.send_message("✅ Thinking mode has been **disabled**.", ephemeral=True)

@app_commands.command(name="showprompts", description="Lists all available preset prompts.")
async def list_prompts(interaction: discord.Interaction):
    bot = interaction.client
    if not bot.prompts:
        await interaction.response.send_message("No predefined prompts found.", ephemeral=True)
        return
    embed = discord.Embed(title="Available System Prompts", color=discord.Color.blue())
    for name, content in bot.prompts.items():
        embed.add_field(name=name, value=f"```{content[:100]}...```", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@app_commands.command(name="help", description="Shows the list of available commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", description="Here are the available slash commands:", color=discord.Color.green())
    embed.add_field(name="/setprompt [name|custom]", value="Sets the bot's system prompt. This disables random mode.", inline=False)
    embed.add_field(name="/prompt", value="Displays the current system prompt or random mode status.", inline=False)
    embed.add_field(name="/random [True|False]", value="Toggles using a random prompt for each reply.", inline=False)
    embed.add_field(name="/think [True|False]", value="Toggles whether the bot shows its thought process (LM Studio only).", inline=False)
    embed.add_field(name="/prompts", value="Lists all available preset prompts.", inline=False)
    embed.add_field(name="/help", value="Shows this help message.", inline=False)
    embed.add_field(name="Mention the bot (@BotName)", value="Ask the bot a question directly by mentioning it.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    """Adds the slash commands to the bot's command tree."""
    bot.tree.add_command(setprompt)
    bot.tree.add_command(prompt)
    bot.tree.add_command(list_prompts)
    bot.tree.add_command(help_command)
    bot.tree.add_command(random_command)
    bot.tree.add_command(think_command)

