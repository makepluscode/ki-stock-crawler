#!/bin/bash

echo "Starting installation..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt update
    sudo apt install -y python3-full python3-pip python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip

# Install specific packages with versions
pip install requests==2.31.0
pip install pandas==2.1.0
pip install python-dotenv==1.0.0
pip install numpy==1.24.3
pip install discord.py==2.3.2
pip install aiohttp==3.9.1
pip install websockets==12.0

# Alternative: Install from requirements.txt
# pip install -r requirements.txt

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Installation completed successfully!"