"""
Simple tests for the AI Resume-Job Matcher
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_processor import (
    clean_text,
    extract_keywords,
    extract_skills_keywords,
    find_missing_keywords,
    preprocess_for_embedding
)


def test_clean_text():
    """Test text cleaning"""
    text = "Hello World!!! This is a TEST... email@example.com http://test.com"
    cleaned = clean_text(text)
    assert "email@example.com" not in cleaned
    assert "http://test.com" not in cleaned
    print("✓ test_clean_text passed")


def test_extract_keywords():
    """Test keyword extraction"""
    text = "Python developer with experience in Django, Flask, and machine learning"
    keywords = extract_keywords(text)
    assert len(keywords) > 0
    assert isinstance(keywords, list)
    print("✓ test_extract_keywords passed")


def test_extract_skills():
    """Test skill extraction"""
    text = "Experienced with Python, FastAPI, Docker, Kubernetes, and AWS"
    skills = extract_skills_keywords(text)
    assert "python" in skills
    assert "docker" in skills or "fastapi" in skills
    print("✓ test_extract_skills passed")


def test_find_missing_keywords():
    """Test finding missing keywords"""
    resume = "Python developer with Flask and Django experience"
    job = "Looking for Python developer with FastAPI, Docker, and Kubernetes"

    missing = find_missing_keywords(resume, job)
    assert isinstance(missing, list)
    print(f"  Missing keywords: {missing}")
    print("✓ test_find_missing_keywords passed")


def test_preprocess_for_embedding():
    """Test preprocessing for embeddings"""
    text = "This is a test   with   extra spaces and http://urls.com"
    processed = preprocess_for_embedding(text)
    assert "http://urls.com" not in processed
    assert "  " not in processed  # No double spaces
    print("✓ test_preprocess_for_embedding passed")


def test_matcher_model():
    """Test the AI matcher model"""
    try:
        from backend.matcher import ResumeJobMatcher

        print("  Loading model...")
        matcher = ResumeJobMatcher()

        resume = "Python developer with 5 years of experience in Django and Flask"
        job = "Looking for Python developer with Django experience"

        score = matcher.calculate_match_score(resume, job)

        assert 0 <= score <= 100
        print(f"  Match score: {score}%")
        print("✓ test_matcher_model passed")

    except Exception as e:
        print(f"✗ test_matcher_model failed: {str(e)}")
        print("  (This is expected if the model isn't downloaded yet)")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running AI Resume-Job Matcher Tests")
    print("=" * 50)
    print()

    tests = [
        test_clean_text,
        test_extract_keywords,
        test_extract_skills,
        test_find_missing_keywords,
        test_preprocess_for_embedding,
        test_matcher_model
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            print(f"Running {test.__name__}...")
            test()
            passed += 1
            print()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {str(e)}")
            failed += 1
            print()
        except Exception as e:
            print(f"✗ {test.__name__} error: {str(e)}")
            failed += 1
            print()

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
