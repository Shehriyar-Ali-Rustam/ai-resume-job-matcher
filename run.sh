#!/bin/bash

# Run both backend and frontend

echo "========================================"
echo "AI Resume-Job Matcher"
echo "========================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ Warning: Virtual environment not found!"
    echo "Run ./setup.sh first"
    exit 1
fi

echo ""
echo "Starting services..."
echo ""

# Start backend in background
echo "Starting FastAPI backend..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    echo "✓ Backend started (PID: $BACKEND_PID)"
    echo "  API: http://localhost:8000"
else
    echo "✗ Failed to start backend"
    exit 1
fi

echo ""

# Start frontend
echo "Starting Streamlit frontend..."
echo "  App: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

streamlit run frontend/app.py

# When Streamlit stops, kill the backend
kill $BACKEND_PID 2>/dev/null
echo ""
echo "Services stopped."
