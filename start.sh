#! /bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Installing dependencies for the current user"
pip install --user -r requirements.txt
echo "Starting bot"

if [ "$RUN_IN_BACKGROUND" = "true" ]; then
    nohup python run_bot.py > output.log 2>&1 &
    echo "Bot is running in the background. Logs are in output.log"
    echo "To stop the bot, run ./stop.sh"
else
    python run_bot.py
fi