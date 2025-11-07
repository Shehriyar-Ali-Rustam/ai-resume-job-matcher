#!/bin/bash

# Start backend in background
echo "Starting FastAPI backend..."
cd backend
python main.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 5

# Start frontend
echo "Starting Streamlit frontend..."
cd ..
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0
