#! /bin/bash

echo "Installing dependencies for the current user"
pip install --user -r requirements.txt
echo "Starting bot"
python main.py