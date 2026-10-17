
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load the model once when this module is imported.
model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Convert a list of text strings into embedding vectors."""

    if not texts:
        return []

    vectors = model.encode(
        texts,
        normalize_embeddings=True
    )

    return vectors.tolist()