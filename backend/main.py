"""
FastAPI backend for AI Resume-Job Matcher
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_processor import (
    extract_text_from_pdf,
    find_missing_keywords,
    extract_keywords,
    preprocess_for_embedding
)
from backend.matcher import ResumeJobMatcher


# Initialize FastAPI app
app = FastAPI(
    title="AI Resume-Job Matcher API",
    description="Free and open-source API for matching resumes with job descriptions using AI",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the matcher (loads the AI model)
matcher = None


@app.on_event("startup")
async def startup_event():
    """Load the AI model on startup"""
    global matcher
    print("Loading AI model...")
    matcher = ResumeJobMatcher()
    print("Model loaded successfully!")


# Request/Response Models
class MatchRequest(BaseModel):
    resume_text: str
    job_description: str


class MatchResponse(BaseModel):
    match_score: float
    missing_keywords: List[str]
    suggestions: str
    resume_keywords: List[str]
    job_keywords: List[str]


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Resume-Job Matcher API",
        "version": "1.0.0",
        "endpoints": {
            "/match": "POST - Match resume with job description (JSON)",
            "/match-file": "POST - Match resume file with job description",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": matcher is not None
    }


@app.post("/match", response_model=MatchResponse)
async def match_resume_job(request: MatchRequest):
    """
    Match a resume with a job description and return analysis.

    Args:
        request: MatchRequest containing resume_text and job_description

    Returns:
        MatchResponse with match score, missing keywords, and suggestions
    """
    try:
        if not matcher:
            raise HTTPException(status_code=503, detail="Model not loaded yet")

        if not request.resume_text or not request.job_description:
            raise HTTPException(
                status_code=400,
                detail="Both resume_text and job_description are required"
            )

        # Preprocess texts
        resume_processed = preprocess_for_embedding(request.resume_text)
        job_processed = preprocess_for_embedding(request.job_description)

        # Calculate match score using AI embeddings
        match_score = matcher.calculate_match_score(resume_processed, job_processed)

        # Extract keywords from both texts
        resume_keywords = extract_keywords(request.resume_text, top_n=15)
        job_keywords = extract_keywords(request.job_description, top_n=15)

        # Find missing keywords
        missing_keywords = find_missing_keywords(request.resume_text, request.job_description)

        # Generate suggestions
        suggestions = generate_suggestions(match_score, missing_keywords)

        return MatchResponse(
            match_score=round(match_score, 2),
            missing_keywords=missing_keywords[:10],  # Limit to top 10
            suggestions=suggestions,
            resume_keywords=resume_keywords,
            job_keywords=job_keywords
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/match-file", response_model=MatchResponse)
async def match_resume_file(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Match a resume file (PDF or TXT) with a job description.

    Args:
        resume_file: Uploaded resume file (PDF or TXT)
        job_description: Job description text

    Returns:
        MatchResponse with match score, missing keywords, and suggestions
    """
    try:
        if not matcher:
            raise HTTPException(status_code=503, detail="Model not loaded yet")

        # Read file content
        file_content = await resume_file.read()

        # Extract text based on file type
        if resume_file.filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_content)
        elif resume_file.filename.lower().endswith('.txt'):
            resume_text = file_content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF or TXT file."
            )

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume")

        # Use the existing match endpoint logic
        request = MatchRequest(resume_text=resume_text, job_description=job_description)
        return await match_resume_job(request)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def generate_suggestions(match_score: float, missing_keywords: List[str]) -> str:
    """
    Generate improvement suggestions based on match score and missing keywords.

    Args:
        match_score: Match score percentage
        missing_keywords: List of missing keywords

    Returns:
        Suggestion text
    """
    suggestions = []

    if match_score >= 85:
        suggestions.append("Excellent match! Your resume aligns very well with the job requirements.")
    elif match_score >= 70:
        suggestions.append("Good match! Your resume shows strong alignment with the job.")
    elif match_score >= 50:
        suggestions.append("Moderate match. Consider enhancing your resume with relevant skills.")
    else:
        suggestions.append("Low match. Significant improvements needed to align with this job.")

    if missing_keywords:
        keywords_str = ", ".join(missing_keywords[:5])
        suggestions.append(
            f"Consider adding these key skills/terms to your resume: {keywords_str}."
        )

        if len(missing_keywords) > 5:
            suggestions.append(
                f"There are {len(missing_keywords) - 5} more relevant keywords to consider."
            )

    if match_score < 70:
        suggestions.append(
            "Tip: Tailor your resume by incorporating keywords from the job description "
            "that match your actual experience."
        )

    return " ".join(suggestions)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
