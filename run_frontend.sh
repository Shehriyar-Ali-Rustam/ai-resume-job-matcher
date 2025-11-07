#!/bin/bash

# Run the Streamlit frontend

echo "Starting Streamlit Frontend..."
echo "App will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the frontend
streamlit run frontend/app.py
