This Discord bot allows you to chat with an AI, powered by either a local model running in LM Studio or the Google Gemini API. It uses slash commands for easy interaction, including the ability to change the AI's personality on the fly with different system prompts.

## Features

- **Dual Backend Support**: Choose between a local LM Studio server or the Google Gemini API.
- **Slash Commands**: Modern and user-friendly `/` commands with autocomplete.
- **Dynamic Personalities**: Use the `/setprompt` command to switch the bot's system prompt instantly from a predefined list or with a custom one.
- **Dynamic Personalities**: Use `/setprompt` to switch the bot's system prompt instantly from a predefined list or with a custom one.
- **Random Prompt Mode**: Use `/random` to have the bot pick a different personality for each reply.
- **Thinking Mode**: Use `/think` to see the bot's thought process (LM Studio only).
- **Easy Startup**: Includes simple startup scripts for both virtual environment and global setups.

## Setup Instructions

Unchanged lines
1.  **Download Project Files**:
    Save all the project files (`main.py`, `bot.py`, `llm_client.py`, etc.) and `requirements.txt` into a single folder on your computer.
    Save all the project files (`main.py`, `bot.py`, `llm_client.py`, `start.sh`, `start_in_venv.sh`, etc.) into a single folder on your computer.

2.  **Install Dependencies**:
    Open a terminal or command prompt in your project folder and run:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Create and Configure the `.env` File**:
    There is a file called `.env.example`. Rename it to `.env` and edit the lines to add your Discord Bot Token and Gemini API Key (if using Gemini).

3.  **Create and Configure the `.env` File**:
    There is a file called .env.example

    Edit the lines on it to add your Discord Bot Token and Gemini API Key (if using Gemini)

    By default it will use LM studio. To use gemini, comment out the LM studio lines and uncomment the Gemini lines.
    
    By default, the bot is configured to use LM Studio. To use Gemini, comment out the LM Studio lines and uncomment the Gemini lines in your `.env` file.

### 5. Run the Bot

1.  **If using LM Studio**:
    - Open LM Studio, select a model, and go to the **Local Server** tab (`<->`).
    - Click **Start Server**.
First, if you are using LM Studio, make sure it's running:
- Open LM Studio, select a model, and go to the **Local Server** tab (`<->`).
- Click **Start Server**.

2.  **Start the Bot**:
    In your terminal, run the main Python script from your project folder:
    ```bash
    python main.py
    ```
    If everything is set up correctly, you'll see messages in your terminal indicating the bot has logged in and synced its commands.
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
    python main.py
    ```

If everything is set up correctly, you'll see messages in your terminal indicating the bot has logged in and synced its commands.

## How to Use the Bot

Interact with the bot in your Discord server using these slash commands:

-   `/help`: Shows a list of all available commands.
-   `/prompts`: Lists all the available preset personalities (system prompts) from the `prompts.json` file.
-   `/showprompts`: Lists all the available preset personalities (system prompts).
-   `/prompt`: Shows the system prompt the bot is currently using.
-   `/setprompt <name>`: Changes the bot's personality. Start typing a name, and it will autocomplete with available presets. You can also type your own custom prompt directly.
-   `/random <True|False>`: Toggles using a random prompt for each reply.
-   `/think <True|False>`: Toggles whether the bot shows its thought process (LM Studio only).
-   **Mention the bot**: You can also have a conversation with the bot by mentioning it directly (e.g., `@YourBotName What is the capital of France?`).






