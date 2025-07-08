This Discord bot allows you to chat with an AI, powered by either a local model running in LM Studio or the Google Gemini API. It uses slash commands for easy interaction, including the ability to change the AI's personality on the fly with different system prompts.

## Features

- **Dual Backend Support**: Choose between a local LM Studio server or the Google Gemini API.
- **Slash Commands**: Modern and user-friendly `/` commands with autocomplete.
- **Dynamic Personalities**: Use `/setprompt` to switch the bot's system prompt instantly from a predefined list or with a custom one.
- **Random Prompt Mode**: Use `/random` to have the bot pick a different personality for each reply.
- **Thinking Mode**: Use `/think` to see the bot's thought process (LM Studio only).
- **Easy Startup**: Includes simple startup scripts for both virtual environment and global setups.
- **Background Operation**: Optionally run the bot as a background process with `nohup`, with logs saved to `output.log`.

## Creating and Inviting Your Discord Bot

Before you can run the bot, you need to create a bot application in the Discord Developer Portal and invite it to your server.

1.  **Create a New Application**:
    *   Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in.
    *   Click the **New Application** button.
    *   Give your application a name (e.g., "My AI Bot") and click **Create**.

2.  **Create a Bot User**:
    *   In your application's dashboard, go to the **Bot** tab on the left-hand menu.
    *   Click the **Add Bot** button and confirm by clicking **Yes, do it!**.

3.  **Get Your Bot Token**:
    *   On the **Bot** tab, you'll see your bot's username and a **Reset Token** button.
    *   Click **Reset Token** and then **Yes, do it!** to reveal your bot's token.
    *   **Copy this token immediately and save it.** This is like a password for your bot, so keep it private. You will need this for the `.env` file later.

4.  **Enable Privileged Intents**:
    *   On the same **Bot** tab, scroll down to the **Privileged Gateway Intents** section.
    *   Enable the **Message Content Intent**. This is required for the bot to read messages.

5.  **Invite the Bot to Your Server**:
    *   Go to the **OAuth2** tab and then click on **URL Generator**.
    *   In the **Scopes** section, check the `bot` and `applications.commands` checkboxes.
    *   In the **Bot Permissions** section that appears, select the following permissions:
        *   **Send Messages**
        *   **Read Message History**
        *   **Use External Emojis**
    *   Scroll down and copy the **Generated URL**.
    *   Paste the URL into your web browser, select the server you want to add the bot to, and click **Authorize**.

Now your bot is in your server and ready to be connected to the code.

## Setup Instructions

1.  **Download Project Files**:
    Save all the project files (`run_bot.py`, `bot.py`, `llm_client.py`, `start.sh`, `start_in_venv.sh`, etc.) into a single folder on your computer.
2.  **Create and Configure the `.env` File**:
    There is a file called `.env.example`. Rename it to `.env` and edit the lines to add your Discord Bot Token and Gemini API Key (if using Gemini).

    By default, the bot is configured to use LM Studio. To use Gemini, comment out the LM Studio lines and uncomment the Gemini lines in your `.env` file.

### 3. Run the Bot

First, if you are using LM Studio, make sure it's running:
- Open LM Studio, select a model, and go to the **Local Server** tab (`<->`).
- Click **Start Server**.

Then, choose one of the following methods to start the bot:

#### Method 1: Using the Startup Scripts (Recommended for Linux/macOS)

The project includes scripts to make starting the bot easy.

**To run in a virtual environment (safest option):**
This script automatically creates a virtual environment, installs dependencies, and runs the bot.
```bash
# Make the script executable (only need to do this once)
chmod +x start_in_venv.sh

# Run the script
./start_in_venv.sh
```

**To run without a virtual environment:**
This script installs dependencies for your user and runs the bot.
```bash
# Make the script executable (only need to do this once)
chmod +x start.sh

# Run the script
./start.sh
```

#### Method 2: Manual Setup (For Windows or other systems)

If you can't use the shell scripts, you can set up and run the bot manually.

1.  **Create and activate a virtual environment (recommended)**:
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it
    # On Windows:
    venv\Scripts\activate
    # On Linux/macOS:
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the Bot**:
    ```bash
    python run_bot.py
    ```

If everything is set up correctly, you'll see messages in your terminal indicating the bot has logged in and synced its commands.

### Running the Bot in the Background

To keep the bot running after you close your terminal, you can run it as a background process.

1.  Open your `.env` file.
2.  Find the line `RUN_IN_BACKGROUND="false"` and change it to `RUN_IN_BACKGROUND="true"`.
3.  Run one of the startup scripts (`./start.sh` or `./start_in_venv.sh`).

The bot will now run in the background. All output and errors will be saved to a file named `output.log`.

To stop the bot, simply run the `stop.sh` script:

```bash
./stop.sh
```

## How to Use the Bot

Interact with the bot in your Discord server using these slash commands:

-   `/help`: Shows a list of all available commands.
-   `/showprompts`: Lists all the available preset personalities (system prompts) from the `prompts.json` file.
-   `/prompt`: Shows the system prompt the bot is currently using.
-   `/setprompt <name>`: Changes the bot's personality. Start typing a name, and it will autocomplete with available presets. You can also type your own custom prompt directly.
-   `/random <True|False>`: Toggles using a random prompt for each reply.
-   `/think <True|False>`: Toggles whether the bot shows its thought process (LM Studio only).
-   **Mention the bot**: You can also have a conversation with the bot by mentioning it directly (e.g., `@YourBotName What is the capital of France?`).