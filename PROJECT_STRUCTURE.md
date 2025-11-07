# Project Structure

```
ai-resume-job-matcher/
│
├── 📄 README.md              # Main documentation
├── 📄 QUICKSTART.md          # Quick start guide
├── 📄 PROJECT_STRUCTURE.md   # This file
├── 📄 LICENSE                # MIT License
├── 📄 .gitignore            # Git ignore rules
├── 📄 requirements.txt       # Python dependencies
│
├── 🔧 setup.sh              # Automated setup script
├── 🔧 run.sh                # Run both backend & frontend
├── 🔧 run_backend.sh        # Run backend only
├── 🔧 run_frontend.sh       # Run frontend only
│
├── 📁 backend/              # FastAPI Backend
│   ├── __init__.py
│   ├── main.py              # API endpoints
│   └── matcher.py           # AI matching logic
│
├── 📁 frontend/             # Streamlit Frontend
│   └── app.py               # Web UI application
│
├── 📁 utils/                # Utility Functions
│   ├── __init__.py
│   └── text_processor.py    # Text processing & NLP
│
├── 📁 models/               # AI Model Scripts
│   └── download_model.py    # Model download utility
│
├── 📁 tests/                # Test Suite
│   ├── __init__.py
│   └── test_matcher.py      # Unit tests
│
└── 📁 samples/              # Sample Data
    ├── sample_resume.txt    # Example resume
    └── sample_job.txt       # Example job description
```

## File Descriptions

### Root Files

- **README.md**: Complete documentation with setup instructions, usage guide, and API reference
- **QUICKSTART.md**: Get started in 5 minutes guide
- **LICENSE**: MIT License for open-source distribution
- **.gitignore**: Excludes unnecessary files from version control
- **requirements.txt**: All Python package dependencies

### Scripts

- **setup.sh**: Automated setup - creates venv, installs dependencies, downloads model
- **run.sh**: Convenience script to run both backend and frontend together
- **run_backend.sh**: Start only the FastAPI backend server
- **run_frontend.sh**: Start only the Streamlit frontend

### Backend (`backend/`)

- **main.py**:
  - FastAPI application with REST API endpoints
  - `/match` - Match resume text with job description
  - `/match-file` - Match uploaded resume file
  - `/health` - API health check

- **matcher.py**:
  - AI matching engine using Sentence Transformers
  - Cosine similarity calculation
  - Embedding generation
  - Batch processing support

### Frontend (`frontend/`)

- **app.py**:
  - Streamlit web interface
  - File upload (PDF/TXT)
  - Text input areas
  - Results visualization
  - Download functionality

### Utils (`utils/`)

- **text_processor.py**:
  - PDF text extraction
  - Text cleaning and preprocessing
  - Keyword extraction (TF-IDF based)
  - Skills extraction (pattern matching)
  - Missing keyword detection
  - Stopwords removal

### Models (`models/`)

- **download_model.py**:
  - Downloads Sentence Transformer model
  - Tests model functionality
  - Shows cache location

### Tests (`tests/`)

- **test_matcher.py**:
  - Unit tests for text processing
  - Integration tests for AI matcher
  - Sample data validation

### Samples (`samples/`)

- **sample_resume.txt**: Example resume for testing (Python Developer)
- **sample_job.txt**: Example job description (Senior Python/ML role)

## Data Flow

```
User Input (Resume + Job Description)
    ↓
Streamlit Frontend (app.py)
    ↓
HTTP Request to FastAPI Backend
    ↓
Text Processing (utils/text_processor.py)
    ↓
AI Matching (backend/matcher.py)
    ├── Embedding Generation
    ├── Cosine Similarity
    └── Keyword Extraction
    ↓
JSON Response
    ↓
Frontend Display (Results, Charts, Suggestions)
    ↓
User Downloads Results
```

## Key Technologies

- **FastAPI**: Modern Python web framework for the API
- **Streamlit**: Simple framework for the web UI
- **Sentence Transformers**: Pre-trained models for semantic similarity
- **NLTK**: Natural language processing toolkit
- **PyPDF2**: PDF text extraction
- **scikit-learn**: Cosine similarity calculations

## Storage

- **AI Model Cache**: `~/.cache/torch/sentence_transformers/`
- **NLTK Data**: `~/nltk_data/`
- **Virtual Environment**: `./venv/`

## Ports Used

- **Backend API**: `http://localhost:8000`
- **Frontend UI**: `http://localhost:8501`

## Next Steps

1. Run `./setup.sh` to install everything
2. Run `./run.sh` to start the application
3. Open `http://localhost:8501` in your browser
4. Start matching resumes!
