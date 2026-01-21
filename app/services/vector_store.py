# File: app/services/vector_store.py
"""
Vector store service using ChromaDB for semantic search.
"""
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.core.logger import get_logger
from app.services.embedding_service import generate_embedding, generate_embeddings

logger = get_logger("TAP.VectorStore")

# Global ChromaDB client
_chroma_client: Optional[chromadb.PersistentClient] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create the ChromaDB client."""
    global _chroma_client
    
    if _chroma_client is None:
        logger.info(f"Initializing ChromaDB at: {settings.CHROMA_PERSIST_DIR}")
        
        # Ensure directory exists
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
        
        _chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        logger.info("ChromaDB initialized successfully.")
    
    return _chroma_client


def get_collection_name(course_id: str) -> str:
    """Generate collection name for a course."""
    # ChromaDB collection names must be 3-63 chars, alphanumeric with underscores
    return f"course_{course_id.replace('-', '_')[:50]}"


def get_or_create_collection(course_id: str) -> chromadb.Collection:
    """Get or create a ChromaDB collection for a course."""
    client = get_chroma_client()
    collection_name = get_collection_name(course_id)
    
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"course_id": course_id}
    )


def add_documents(
    course_id: str,
    documents: List[str],
    metadatas: List[Dict[str, Any]],
    ids: List[str]
) -> List[str]:
    """
    Add documents to the vector store.
    
    Args:
        course_id: Course ID for collection
        documents: List of text documents
        metadatas: List of metadata dicts for each document
        ids: Unique IDs for each document
    
    Returns:
        List of document IDs that were added
    """
    if not documents:
        return []
    
    collection = get_or_create_collection(course_id)
    
    logger.info(f"Adding {len(documents)} documents to collection for course {course_id}")
    
    # Generate embeddings
    embeddings = generate_embeddings(documents)
    
    # Add to ChromaDB
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    logger.info(f"Added {len(documents)} documents successfully.")
    
    return ids


def search_documents(
    course_id: str,
    query: str,
    n_results: int = 5,
    filter_metadata: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search for similar documents in the vector store.
    
    Args:
        course_id: Course ID to search in
        query: Search query text
        n_results: Number of results to return
        filter_metadata: Optional metadata filter (e.g., {"source": "lecture"})
    
    Returns:
        List of search results with document, metadata, and distance
    """
    collection = get_or_create_collection(course_id)
    
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # Search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=filter_metadata if filter_metadata else None,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format results
    search_results = []
    if results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            search_results.append({
                "id": doc_id,
                "document": results["documents"][0][i] if results["documents"] else None,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            })
    
    return search_results


def delete_documents(course_id: str, ids: List[str]) -> bool:
    """
    Delete documents from the vector store.
    
    Args:
        course_id: Course ID
        ids: List of document IDs to delete
    
    Returns:
        True if successful
    """
    if not ids:
        return True
    
    collection = get_or_create_collection(course_id)
    collection.delete(ids=ids)
    
    logger.info(f"Deleted {len(ids)} documents from course {course_id}")
    return True


def delete_collection(course_id: str) -> bool:
    """
    Delete entire collection for a course.
    
    Args:
        course_id: Course ID
    
    Returns:
        True if successful
    """
    client = get_chroma_client()
    collection_name = get_collection_name(course_id)
    
    try:
        client.delete_collection(collection_name)
        logger.info(f"Deleted collection: {collection_name}")
        return True
    except Exception as e:
        logger.warning(f"Error deleting collection: {str(e)}")
        return False


def get_collection_stats(course_id: str) -> Dict[str, Any]:
    """
    Get statistics for a course's vector collection.
    
    Args:
        course_id: Course ID
    
    Returns:
        Dictionary with collection statistics
    """
    collection = get_or_create_collection(course_id)
    
    return {
        "course_id": course_id,
        "collection_name": collection.name,
        "document_count": collection.count(),
    }
