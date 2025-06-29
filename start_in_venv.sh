#! /bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment in 'venv'..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Starting bot"
python main.py
