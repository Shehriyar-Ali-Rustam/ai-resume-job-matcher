# 🎯 AI Resume-Job Matcher - Free Online Resume Matching Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-resume-matcher.streamlit.app)

**🚀 Try it now:** [https://ai-resume-matcher.streamlit.app](https://ai-resume-matcher.streamlit.app)

**100% Free, Open Source, and Privacy-Focused Resume Analysis Tool**

An AI-powered web application that compares your resume with job descriptions using Natural Language Processing (NLP) and provides actionable insights to improve your job application success rate. Perfect for job seekers, career changers, and anyone looking to optimize their resume for ATS systems.

## 🌟 Live Demo

Visit [ai-resume-matcher.streamlit.app](https://ai-resume-matcher.streamlit.app) to use the tool instantly - no sign-up or installation required!

## ✨ Features

- 🤖 **AI-Powered Matching**: Uses Sentence Transformers for semantic similarity analysis
- 📊 **Match Score**: Get a 0-100% compatibility score
- 🔍 **Missing Skills Detection**: Identifies keywords and skills present in job description but missing from your resume
- 💡 **Smart Suggestions**: AI-generated recommendations to improve your resume
- 🔒 **Privacy First**: All processing happens locally on your machine - no data sent to external servers
- 📄 **Multiple Formats**: Supports PDF and TXT resume files
- 💾 **Export Results**: Download your analysis as a text file
- 🎨 **Modern UI**: Clean, responsive interface built with Streamlit
- ⚡ **Fast & Free**: No API costs, runs entirely offline after initial setup

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Backend**: FastAPI (REST API)
- **Frontend**: Streamlit (Web UI)
- **AI Model**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **NLP**: NLTK, spaCy
- **PDF Processing**: PyPDF2
- **ML**: scikit-learn
- **Platform**: Ubuntu (works on Windows/Mac too)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 2GB free disk space (for AI model)
- Internet connection (only for initial setup)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-job-matcher.git
cd ai-resume-job-matcher
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Ubuntu/Mac
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download AI Model (First Time Only)

```bash
python models/download_model.py
```

This will download the `all-MiniLM-L6-v2` model (~90MB). It only needs to be done once.

### 5. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

## 🎮 Running the Application

You need to run **both** the backend and frontend:

### Option 1: Using Two Terminals (Recommended)

**Terminal 1 - Backend API:**
```bash
cd backend
python main.py
```

The API will start at `http://localhost:8000`

**Terminal 2 - Frontend UI:**
```bash
streamlit run frontend/app.py
```

The web app will open at `http://localhost:8501`

### Option 2: Using Background Process

```bash
# Start backend in background
cd backend && python main.py &

# Start frontend
streamlit run frontend/app.py
```

## 📖 How to Use

1. **Open the web app** at `http://localhost:8501`
2. **Upload your resume** (PDF or TXT) or paste the text
3. **Paste the job description** you want to match against
4. **Click "Check Match"**
5. **View results**:
   - Match score percentage
   - Missing keywords/skills
   - AI-generated suggestions
   - Resume and job keywords
6. **Download results** as a text file (optional)

## 📁 Project Structure

```
ai-resume-job-matcher/
│
├── backend/               # FastAPI backend
│   ├── main.py           # API endpoints
│   ├── matcher.py        # AI matching logic
│   └── __init__.py
│
├── frontend/             # Streamlit frontend
│   └── app.py           # Web UI
│
├── utils/               # Utility functions
│   ├── text_processor.py  # Text cleaning, keyword extraction
│   └── __init__.py
│
├── models/              # AI model scripts
│   └── download_model.py  # Model download script
│
├── samples/             # Sample files for testing
│   ├── sample_resume.txt
│   └── sample_job.txt
│
├── tests/               # Test files (optional)
│
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🧪 Testing with Sample Data

We've included sample files for testing:

**Sample Resume:**
```
Python Developer with 5 years of experience in building web applications.
Skilled in Flask, Django, SQL, and Machine Learning.
Experience with data analysis using pandas and numpy.
```

**Sample Job Description:**
```
Looking for a Python Developer with experience in FastAPI, Docker, and NLP.
Must have strong understanding of RESTful APIs and microservices.
Experience with AWS and CI/CD pipelines is a plus.
```

**Expected Output:**
- Match Score: ~70-75%
- Missing Keywords: FastAPI, Docker, NLP, AWS, RESTful APIs, microservices
- Suggestions: Add FastAPI, Docker, and NLP experience to improve match

## 🔧 API Endpoints

### GET `/`
- Returns API information

### GET `/health`
- Health check endpoint

### POST `/match`
- Match resume text with job description
- **Body**: `{"resume_text": "...", "job_description": "..."}`
- **Returns**: Match score, missing keywords, suggestions

### POST `/match-file`
- Match resume file with job description
- **Form Data**: `resume_file` (PDF/TXT), `job_description` (text)
- **Returns**: Same as `/match`

## 🎨 Customization

### Change AI Model

Edit [backend/matcher.py](backend/matcher.py):

```python
# Try different models from sentence-transformers
matcher = ResumeJobMatcher(model_name='paraphrase-MiniLM-L6-v2')
```

### Adjust Keyword Extraction

Edit [utils/text_processor.py](utils/text_processor.py) to add more skills or customize extraction logic.

### Customize UI

Edit [frontend/app.py](frontend/app.py) to change colors, layout, or add new features.

## 🌐 Deployment Options

### Local Network (Share with Friends)

Use ngrok for temporary public URL:

```bash
# Install ngrok
sudo snap install ngrok

# Expose Streamlit
ngrok http 8501
```

### Hugging Face Spaces (Free Cloud Hosting)

1. Create account on [Hugging Face](https://huggingface.co)
2. Create new Space (Streamlit)
3. Upload your code
4. Done! Free hosting forever

### Docker (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "python backend/main.py & streamlit run frontend/app.py"]
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### API Not Running
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Model Download Fails
```bash
# Manually download
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### NLTK Data Missing
```bash
python -c "import nltk; nltk.download('all')"
```

### Permission Errors on Ubuntu
```bash
# Install with user flag
pip install --user -r requirements.txt
```

## 🔮 Future Improvements

- [ ] Support for multiple resume comparison
- [ ] Cover letter analysis
- [ ] LinkedIn profile integration
- [ ] ATS (Applicant Tracking System) simulation
- [ ] Industry-specific keyword databases
- [ ] Resume template suggestions
- [ ] Multi-language support
- [ ] Dark mode UI
- [ ] Export to PDF with formatting
- [ ] Historical analysis tracking

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) for the amazing NLP models
- [FastAPI](https://fastapi.tiangolo.com/) for the modern API framework
- [Streamlit](https://streamlit.io/) for the easy-to-use UI framework
- [Hugging Face](https://huggingface.co/) for hosting free models

## 📧 Contact

Have questions or suggestions? Feel free to:
- Open an issue
- Submit a pull request
- Contact the maintainers

## ⭐ Star History

If you find this project helpful, please give it a star! It helps others discover this tool.

---

**Made with ❤️ by the community | 100% Free & Open Source**

*No paid APIs • No data collection • No hidden costs*
