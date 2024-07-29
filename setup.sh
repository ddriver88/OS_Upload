#!/bin/bash

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    # Create virtual environment
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed."

# Run the main application
streamlit run LeadUploadFormatter2_0.py