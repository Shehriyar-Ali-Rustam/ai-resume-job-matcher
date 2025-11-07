"""
Script to download the AI model (Sentence Transformer).
This will download the model the first time you run it.
"""

from sentence_transformers import SentenceTransformer
import os


def download_model(model_name='all-MiniLM-L6-v2'):
    """
    Download the sentence transformer model.

    Args:
        model_name: Name of the model to download (default: all-MiniLM-L6-v2)
    """
    print(f"Downloading model: {model_name}")
    print("This may take a few minutes on the first run...")
    print("-" * 50)

    try:
        # This will download the model if not already cached
        model = SentenceTransformer(model_name)

        print("\n✅ Model downloaded successfully!")
        print(f"Model name: {model_name}")
        print(f"Max sequence length: {model.max_seq_length}")
        print(f"Embedding dimension: {model.get_sentence_embedding_dimension()}")

        # Test the model
        print("\n🧪 Testing model...")
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        print(f"Test embedding shape: {embedding.shape}")

        print("\n✨ Model is ready to use!")
        print(f"Cache location: {os.path.expanduser('~/.cache/torch/sentence_transformers/')}")

        return model

    except Exception as e:
        print(f"\n❌ Error downloading model: {str(e)}")
        print("\nPlease check your internet connection and try again.")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("AI Resume-Job Matcher - Model Download")
    print("=" * 50)
    print()

    download_model()

    print("\n" + "=" * 50)
    print("You can now run the application!")
    print("=" * 50)
