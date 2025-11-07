"""
Text processing utilities for resume and job description analysis.
"""

import re
import string
from typing import List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import PyPDF2
from io import BytesIO


# Download required NLTK data (only first time)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file content.

    Args:
        file_content: PDF file content as bytes

    Returns:
        Extracted text as string
    """
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


def clean_text(text: str) -> str:
    """
    Clean text by removing special characters, extra spaces, and lowercasing.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove special characters but keep alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9\s+#\-]', ' ', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text


def remove_stopwords(text: str) -> str:
    """
    Remove common stopwords from text.

    Args:
        text: Input text

    Returns:
        Text with stopwords removed
    """
    try:
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        # Keep important technical words even if they're in stopwords
        important_words = {'python', 'r', 'c', 'go', 'ai', 'ml', 'will', 'can'}
        stop_words = stop_words - important_words

        filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
        return ' '.join(filtered_text)
    except Exception as e:
        # If tokenization fails, return cleaned text
        return text


def extract_keywords(text: str, top_n: int = 20) -> List[str]:
    """
    Extract important keywords from text using simple frequency analysis.

    Args:
        text: Input text
        top_n: Number of top keywords to extract

    Returns:
        List of keywords
    """
    from collections import Counter

    # Clean the text
    cleaned_text = clean_text(text)

    # Tokenize
    words = cleaned_text.split()

    # Remove very short words (likely not meaningful)
    words = [w for w in words if len(w) > 2]

    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w not in stop_words]
    except:
        pass

    # Count frequency
    word_freq = Counter(words)

    # Get top keywords
    top_keywords = [word for word, _ in word_freq.most_common(top_n)]

    return top_keywords


def extract_skills_keywords(text: str) -> Set[str]:
    """
    Extract technical skills and important keywords from text.
    Uses pattern matching for common skills and technologies.

    Args:
        text: Input text

    Returns:
        Set of identified skills/keywords
    """
    text_lower = text.lower()
    skills = set()

    # Common programming languages
    languages = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
        'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html',
        'css', 'bash', 'shell', 'perl'
    ]

    # Frameworks and libraries
    frameworks = [
        'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'node.js', 'express', 'next.js', 'laravel', 'rails', 'asp.net',
        'streamlit', 'gradio', 'huggingface', 'transformers'
    ]

    # Tools and technologies
    tools = [
        'git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp',
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'kafka',
        'spark', 'hadoop', 'airflow', 'linux', 'unix', 'agile', 'scrum',
        'ci/cd', 'devops', 'mlops', 'rest', 'api', 'graphql', 'microservices'
    ]

    # AI/ML specific
    ai_ml = [
        'machine learning', 'deep learning', 'neural network', 'nlp',
        'computer vision', 'data science', 'artificial intelligence',
        'natural language processing', 'reinforcement learning', 'lstm',
        'transformer', 'bert', 'gpt', 'llm', 'generative ai'
    ]

    # Check for all skill categories
    all_skills = languages + frameworks + tools + ai_ml

    for skill in all_skills:
        if skill in text_lower:
            skills.add(skill)

    # Extract other keywords using word patterns
    words = re.findall(r'\b[a-z][a-z0-9+#\-]*\b', text_lower)

    # Add multi-word technical terms
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]

    for term in bigrams + trigrams:
        if any(tech in term for tech in ['machine learning', 'deep learning', 'data science', 'computer vision']):
            skills.add(term)

    return skills


def find_missing_keywords(resume_text: str, job_text: str) -> List[str]:
    """
    Find keywords present in job description but missing from resume.

    Args:
        resume_text: Resume text
        job_text: Job description text

    Returns:
        List of missing keywords
    """
    resume_skills = extract_skills_keywords(resume_text)
    job_skills = extract_skills_keywords(job_text)

    # Find skills in job but not in resume
    missing = job_skills - resume_skills

    return sorted(list(missing))


def preprocess_for_embedding(text: str) -> str:
    """
    Preprocess text for embedding generation.
    Less aggressive cleaning to preserve context.

    Args:
        text: Input text

    Returns:
        Preprocessed text
    """
    # Remove URLs and emails
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text
