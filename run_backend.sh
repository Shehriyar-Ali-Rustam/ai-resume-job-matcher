#!/bin/bash

# Run the FastAPI backend

echo "Starting FastAPI Backend..."
echo "API will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the backend
cd backend
python main.py
