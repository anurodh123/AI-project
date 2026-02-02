#!/bin/bash
# Quick start script for Snake AI training

echo "=========================================="
echo "Snake Game AI - Q-Learning Project"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Dependencies installed successfully!"
echo ""
echo "You can now:"
echo "1. Run the main menu: python main.py"
echo "2. Train the agent: python training/train.py"
echo "3. Test the agent: python training/test.py"
echo "4. View visualizations: python -c 'from utils.visualization import *; plot_training_progress()'"
echo ""
echo "For more information, see README.md"
