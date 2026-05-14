#!/usr/bin/env bash
# Run once to bootstrap the project
set -e

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Done! Next steps:"
echo "  1. Copy .env.example to .env and add your Anthropic API key"
echo "  2. Drop your credentials.json into this folder"
echo "  3. Run: source venv/bin/activate && python tracker.py"
