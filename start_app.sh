#!/bin/bash

# Start the Trip Itinerary PDF Generator Web UI

echo "🚀 Starting Trip Itinerary PDF Generator..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Add Python bin to PATH if not already there
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Run streamlit
python3 -m streamlit run app.py

