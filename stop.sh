#!/bin/bash

echo "Attempting to stop the bot..."
# Find the process running 'python main.py' and kill it
PID=$(pgrep -f "python run_bot.py")

if [ -z "$PID" ]; then
    echo "Bot process not found."
else
    kill $PID
    echo "Bot process with PID $PID has been stopped."
fi
