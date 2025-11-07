"""
AI-powered resume and job description matcher using Sentence Transformers.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Tuple
import os


class ResumeJobMatcher:
    """
    AI matcher using Sentence Transformers for semantic similarity.
    Uses the free 'all-MiniLM-L6-v2' model that runs offline.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the matcher with a sentence transformer model.

        Args:
            model_name: Name of the sentence transformer model to use
        """
        print(f"Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")

    def calculate_match_score(self, resume_text: str, job_text: str) -> float:
        """
        Calculate semantic similarity match score between resume and job description.

        Args:
            resume_text: Resume text
            job_text: Job description text

        Returns:
            Match score as percentage (0-100)
        """
        # Generate embeddings for both texts
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=False)
        job_embedding = self.model.encode(job_text, convert_to_tensor=False)

        # Reshape for sklearn
        resume_embedding = resume_embedding.reshape(1, -1)
        job_embedding = job_embedding.reshape(1, -1)

        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]

        # Convert to percentage (0-100)
        match_score = float(similarity * 100)

        return max(0.0, min(100.0, match_score))  # Ensure it's within 0-100

    def calculate_section_scores(
        self,
        resume_sections: List[str],
        job_sections: List[str]
    ) -> List[Tuple[float, str, str]]:
        """
        Calculate match scores for different sections of resume and job description.

        Args:
            resume_sections: List of resume section texts
            job_sections: List of job description section texts

        Returns:
            List of tuples (score, resume_section, job_section)
        """
        scores = []

        for r_section in resume_sections:
            for j_section in job_sections:
                if r_section.strip() and j_section.strip():
                    score = self.calculate_match_score(r_section, j_section)
                    scores.append((score, r_section[:100], j_section[:100]))

        return sorted(scores, reverse=True)

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding vector for a given text.

        Args:
            text: Input text

        Returns:
            Embedding vector as numpy array
        """
        return self.model.encode(text, convert_to_tensor=False)

    def batch_calculate_scores(
        self,
        resume_text: str,
        job_descriptions: List[str]
    ) -> List[Tuple[int, float]]:
        """
        Calculate match scores for one resume against multiple job descriptions.

        Args:
            resume_text: Resume text
            job_descriptions: List of job description texts

        Returns:
            List of tuples (index, score) sorted by score descending
        """
        resume_embedding = self.get_embedding(resume_text)

        scores = []
        for idx, job_text in enumerate(job_descriptions):
            if job_text.strip():
                job_embedding = self.get_embedding(job_text)

                resume_emb = resume_embedding.reshape(1, -1)
                job_emb = job_embedding.reshape(1, -1)

                similarity = cosine_similarity(resume_emb, job_emb)[0][0]
                match_score = float(similarity * 100)

                scores.append((idx, match_score))

        return sorted(scores, key=lambda x: x[1], reverse=True)
