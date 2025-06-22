# Discord AI Chat Bot

This Discord bot allows you to chat with an AI, powered by either a local model running in LM Studio or the Google Gemini API. It uses slash commands for easy interaction, including the ability to change the AI's personality on the fly with different system prompts.

## Features

- **Dual Backend Support**: Choose between a local LM Studio server or the Google Gemini API.
- **Slash Commands**: Modern and user-friendly `/` commands with autocomplete.
- **Dynamic Personalities**: Use the `/setprompt` command to switch the bot's system prompt instantly from a predefined list or with a custom one.
- **Easy to Configure**: Switch providers and set API keys using a simple `.env` file.

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or newer.
- A Discord account with a server you can manage.
- **For LM Studio**:
    - [LM Studio](https://lmstudio.ai/) installed and running on your computer.
- **For Gemini API**:
    - A Google Gemini API key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Create a Discord Bot Application

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click **New Application** and give it a name.
3.  Navigate to the **Bot** tab on the left.
4.  Under **Privileged Gateway Intents**, enable the **MESSAGE CONTENT INTENT**.
5.  Click **Reset Token** to generate a new bot token and copy it. **This is your `DISCORD_BOT_TOKEN`**. Keep it safe.

### 3. Invite the Bot to Your Server

1.  In the Discord Developer Portal, go to **OAuth2 -> URL Generator**.
2.  In the "Scopes" box, select `bot` and `applications.commands`.
3.  A "Bot Permissions" box will appear below. Select **Send Messages** and **Read Message History**.
4.  Copy the generated URL, paste it into your browser, and invite the bot to your Discord server.

### 4. Project Setup and Configuration

1.  **Download Project Files**:
    Save all the project files (`main.py`, `bot.py`, `llm_client.py`, etc.) and `requirements.txt` into a single folder on your computer.

2.  **Install Dependencies**:
    Open a terminal or command prompt in your project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create and Configure the `.env` File**:
    There is a file called .env.example

    Edit the lines on it to add your Discord Bot Token and Gemini API Key (if using Gemini)

    By default it will use LM studio. To use gemini, comment out the LM studio lines and uncomment the Gemini lines.
    

### 5. Run the Bot

1.  **If using LM Studio**:
    - Open LM Studio, select a model, and go to the **Local Server** tab (`<->`).
    - Click **Start Server**.

2.  **Start the Bot**:
    In your terminal, run the main Python script from your project folder:
    ```bash
    python main.py
    ```
    If everything is set up correctly, you'll see messages in your terminal indicating the bot has logged in and synced its commands.

## How to Use the Bot

Interact with the bot in your Discord server using these slash commands:

-   `/help`: Shows a list of all available commands.
-   `/prompts`: Lists all the available preset personalities (system prompts) from the `prompts.json` file.
-   `/prompt`: Shows the system prompt the bot is currently using.
-   `/setprompt <name>`: Changes the bot's personality. Start typing a name, and it will autocomplete with available presets. You can also type your own custom prompt directly.
-   **Mention the bot**: You can also have a conversation with the bot by mentioning it directly (e.g., `@YourBotName What is the capital of France?`).

Enjoy your custom AI chat bot!


