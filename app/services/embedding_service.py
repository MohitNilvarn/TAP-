# File: app/services/embedding_service.py
"""
Embedding service using HuggingFace sentence-transformers.
Uses local models for privacy and no API costs.
"""
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.EmbeddingService")

# Global model instance (lazy loaded)
_embedding_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """
    Get or create the embedding model instance.
    Uses 'all-MiniLM-L6-v2' by default - fast and good quality.
    """
    global _embedding_model
    
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding model loaded successfully.")
    
    return _embedding_model


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text.
    
    Args:
        text: Input text to embed
    
    Returns:
        List of float values (embedding vector)
    """
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def generate_embeddings(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently.
    
    Args:
        texts: List of texts to embed
        batch_size: Batch size for processing (affects memory usage)
    
    Returns:
        List of embedding vectors
    """
    if not texts:
        return []
    
    model = get_embedding_model()
    
    logger.info(f"Generating embeddings for {len(texts)} texts...")
    
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    
    logger.info("Embeddings generated successfully.")
    
    return [emb.tolist() for emb in embeddings]


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
    
    Returns:
        Cosine similarity score (0 to 1)
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))


def find_most_similar(
    query_embedding: List[float],
    document_embeddings: List[List[float]],
    top_k: int = 5
) -> List[tuple]:
    """
    Find the most similar documents to a query.
    
    Args:
        query_embedding: Query embedding vector
        document_embeddings: List of document embedding vectors
        top_k: Number of top results to return
    
    Returns:
        List of (index, similarity_score) tuples, sorted by similarity
    """
    if not document_embeddings:
        return []
    
    similarities = []
    for idx, doc_emb in enumerate(document_embeddings):
        sim = compute_similarity(query_embedding, doc_emb)
        similarities.append((idx, sim))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_k]


def get_embedding_dimension() -> int:
    """Get the dimension of embeddings from the current model."""
    model = get_embedding_model()
    return model.get_sentence_embedding_dimension()
