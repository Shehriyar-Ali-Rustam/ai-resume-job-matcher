# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Setup (One-time)

```bash
# Run the automated setup script
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download the AI model
- Download NLTK data

## Step 2: Run the Application

### Option A: Run Everything Together (Easiest)

```bash
./run.sh
```

This starts both the backend and frontend automatically.

### Option B: Run Separately (Two Terminals)

**Terminal 1:**
```bash
./run_backend.sh
```

**Terminal 2:**
```bash
./run_frontend.sh
```

## Step 3: Use the App

1. Open your browser to `http://localhost:8501`
2. Upload your resume or paste the text
3. Paste the job description
4. Click "Check Match"
5. View your results!

## Testing with Sample Data

Try the included sample files:
- Resume: `samples/sample_resume.txt`
- Job: `samples/sample_job.txt`

## Troubleshooting

### Port Already in Use

```bash
# Find and kill the process using port 8000
lsof -i :8000
kill -9 <PID>

# Or for port 8501
lsof -i :8501
kill -9 <PID>
```

### Dependencies Issue

```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Model Not Loading

```bash
# Re-download the model
python models/download_model.py
```

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
