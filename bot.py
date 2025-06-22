# bot.py
import discord
from discord.ext import commands
from llm_client import get_llm_response
import json

class LLMBot(commands.Bot):
    """
    A Discord bot that interacts with an LLM and allows changing system prompts.
    """
    def __init__(self, command_prefix: str, lm_studio_url: str):
        """
        Initializes the bot.
        """
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix=command_prefix, intents=intents)

        self.lm_studio_url = lm_studio_url
        self.prompts = self.load_prompts()
        self.system_prompt = self.prompts.get("default", "You are a helpful assistant.")
        
        # Remove the default help command to create a custom one if needed
        self.remove_command('help')
        self.add_commands()

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

    def add_commands(self):
        """A helper function to define and add commands to the bot."""

        @self.command(name='setprompt', help='Sets the system prompt for the bot. Usage: !setprompt <prompt_name_or_custom_prompt>')
        async def setprompt(ctx, *, prompt_input: str):
            if prompt_input in self.prompts:
                self.system_prompt = self.prompts[prompt_input]
                await ctx.send(f"System prompt changed to **{prompt_input}**.")
            else:
                self.system_prompt = prompt_input
                await ctx.send(f"Custom system prompt set!")

        @self.command(name='prompt', help='Shows the current system prompt.')
        async def prompt(ctx):
            await ctx.send(f"**Current System Prompt:**\n```\n{self.system_prompt}\n```")

        @self.command(name='prompts', help='Lists all available preset prompts.')
        async def list_prompts(ctx):
            if not self.prompts:
                await ctx.send("No predefined prompts found.")
                return

            embed = discord.Embed(title="Available System Prompts", color=discord.Color.blue())
            for name, content in self.prompts.items():
                embed.add_field(name=name, value=f"```{content[:100]}...```", inline=False)
            await ctx.send(embed=embed)
            
        @self.command(name='help')
        async def help_command(ctx):
            embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.green())
            embed.add_field(name=f"{self.command_prefix}setprompt <name|custom>", value="Sets the bot's system prompt. Use a preset name or type your own.", inline=False)
            embed.add_field(name=f"{self.command_prefix}prompt", value="Displays the current system prompt.", inline=False)
            embed.add_field(name=f"{self.command_prefix}prompts", value="Lists all available preset prompts.", inline=False)
            embed.add_field(name="Mention the bot (@BotName)", value="Ask the bot a question directly by mentioning it.", inline=False)
            await ctx.send(embed=embed)


    async def on_ready(self):
        """Called when the bot has successfully connected to Discord."""
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print('Bot is ready to receive messages and commands.')
        print('------')

    async def on_message(self, message: discord.Message):
        """Called whenever a message is sent."""
        if message.author == self.user:
            return

        # Process commands first
        await self.process_commands(message)

        # Then, check for mentions if it wasn't a command
        if not message.content.startswith(self.command_prefix) and self.user.mentioned_in(message):
            async with message.channel.typing():
                try:
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

