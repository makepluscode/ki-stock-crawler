#!/bin/bash

echo "Starting installation..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
. ./venv/bin/activate

# Install required packages
echo "Installing required packages..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Deactivate virtual environment
deactivate

echo "Installation completed successfully!"