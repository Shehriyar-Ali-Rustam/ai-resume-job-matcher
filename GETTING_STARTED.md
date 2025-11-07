# Getting Started with AI Resume-Job Matcher

Welcome! This guide will help you set up and run the AI Resume-Job Matcher on your Ubuntu machine.

## What You'll Get

- A web-based resume analysis tool
- AI-powered matching (0-100% score)
- Missing skills detection
- Actionable improvement suggestions
- 100% free and runs offline

## Prerequisites Check

Before starting, make sure you have:

```bash
# Check Python version (need 3.8+)
python3 --version

# Check pip
pip3 --version

# Check available disk space (need ~2GB)
df -h .
```

If Python is missing:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## Installation (3 Steps)

### Step 1: Navigate to Project Directory

```bash
cd "/home/shehriyar-ali-rustam/AI powered resume and job matcher"
```

### Step 2: Run Setup Script

```bash
./setup.sh
```

This takes 5-10 minutes and will:
- Create a Python virtual environment
- Install all required packages
- Download the AI model (~90MB)
- Download NLP data
- Verify everything works

### Step 3: Start the Application

```bash
./run.sh
```

This will start both the backend and frontend automatically.

**Alternative**: Run in separate terminals:

Terminal 1:
```bash
./run_backend.sh
```

Terminal 2:
```bash
./run_frontend.sh
```

## First Use

1. The app will automatically open at `http://localhost:8501`
2. You'll see a clean interface with two main sections

### Try It Out!

**Quick Test with Sample Data:**

1. Click "Paste Text" for resume input
2. Copy the content from `samples/sample_resume.txt`
3. Paste it in the resume field
4. Copy the content from `samples/sample_job.txt`
5. Paste it in the job description field
6. Click "Check Match"

You should see:
- Match score around 70-75%
- Missing keywords like "FastAPI", "Docker", "NLP"
- AI-generated suggestions for improvement

### Use Your Own Resume

**Option A - Upload File:**
1. Select "Upload File"
2. Choose your PDF or TXT resume
3. Paste the job description
4. Click "Check Match"

**Option B - Paste Text:**
1. Select "Paste Text"
2. Copy-paste your resume
3. Paste the job description
4. Click "Check Match"

## Understanding Your Results

### Match Score
- **85-100%**: Excellent match - apply confidently!
- **70-84%**: Good match - minor improvements possible
- **50-69%**: Moderate match - add relevant skills
- **0-49%**: Low match - consider significant updates

### Missing Keywords
Red-highlighted terms found in job description but not in your resume.

**Pro Tip**: Only add keywords if they match your actual experience!

### Resume Keywords
Skills and terms extracted from your resume (blue boxes).

### Job Keywords
Important terms from the job description (orange boxes).

### AI Suggestions
Personalized recommendations based on the analysis.

## Features to Explore

### Download Results
Click "Download as TXT" to save your analysis for later reference.

### Compare Multiple Jobs
Run your resume against different job descriptions to see which fits best.

### Iterate and Improve
Update your resume based on suggestions and re-run the analysis.

## Troubleshooting

### "Backend API is not running"

The backend server isn't started. Run:
```bash
./run_backend.sh
```

Wait for the message "Model loaded successfully!" before opening the frontend.

### "Could not extract text from PDF"

Try these solutions:
1. Re-save your PDF (File → Save As)
2. Convert to TXT and paste text directly
3. Use a different PDF viewer to re-export

### Port Already in Use

Someone else is using port 8000 or 8501:

```bash
# Find the process
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Slow First Run

The first analysis takes longer (10-15 seconds) as the model loads. Subsequent runs are much faster (2-3 seconds).

### Model Download Failed

Rerun the model download:
```bash
source venv/bin/activate
python models/download_model.py
```

## Tips for Best Results

1. **Use Complete Resumes**: Include all sections (experience, skills, education)
2. **Clean Job Descriptions**: Copy the full JD, not just bullet points
3. **Be Specific**: The AI works better with detailed information
4. **Multiple Runs**: Test different versions of your resume
5. **Honest Updates**: Only add skills you actually possess

## Command Reference

```bash
# Setup (one time)
./setup.sh

# Run everything
./run.sh

# Run backend only
./run_backend.sh

# Run frontend only
./run_frontend.sh

# Run tests
source venv/bin/activate
python tests/test_matcher.py

# Stop everything
# Press Ctrl+C in the terminal
```

## What's Happening Behind the Scenes?

1. **Text Extraction**: Your resume is converted to plain text
2. **Preprocessing**: Text is cleaned and normalized
3. **Embedding Generation**: AI converts text to numerical vectors
4. **Similarity Calculation**: Cosine similarity measures how close the vectors are
5. **Keyword Extraction**: NLP identifies important terms
6. **Comparison**: Keywords in job vs keywords in resume
7. **Suggestion Generation**: AI creates personalized recommendations

## Privacy & Security

- All processing happens on your machine
- No data is sent to external servers
- Your resume stays private
- No accounts or login required
- No tracking or analytics

## Next Steps

1. **Customize**: Edit the code to add your own features
2. **Share**: Deploy for friends using ngrok or Hugging Face Spaces
3. **Contribute**: Improve the project and share back
4. **Star**: Give the project a star if you find it useful!

## Need More Help?

- Check [README.md](README.md) for detailed documentation
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for code organization
- See [QUICKSTART.md](QUICKSTART.md) for the shortest path to running
- Open an issue on GitHub for bugs or questions

## Example Workflow

```
1. Job searching → Find interesting position
2. Copy job description
3. Open AI Resume-Job Matcher
4. Upload/paste your resume
5. Paste job description
6. Get match score + insights
7. Update resume based on suggestions
8. Re-run analysis
9. Download results
10. Apply with confidence!
```

## Performance Expectations

- **Setup Time**: 5-10 minutes (one time)
- **Model Download**: 2-3 minutes (one time)
- **First Analysis**: 10-15 seconds (model loading)
- **Subsequent Analyses**: 2-3 seconds
- **Memory Usage**: ~500MB RAM
- **Disk Space**: ~2GB total

---

Ready to match your resume? Run `./setup.sh` to begin!

**Questions?** Check the README or open an issue.

**Happy job hunting!** 🎯
