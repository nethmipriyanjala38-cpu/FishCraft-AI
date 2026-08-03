"""
FishCraft AI - Embeddings
Uses sentence-transformers to generate embeddings for the RAG pipeline.
This is lightweight and free, ideal for Streamlit Cloud deployment.
"""

from chromadb.utils import embedding_functions

# We use the default ChromaDB embedding function which under the hood uses
# sentence-transformers (all-MiniLM-L6-v2). It's fast, small, and effective.
def get_embedding_function():
    """Return the embedding function for ChromaDB."""
    return embedding_functions.DefaultEmbeddingFunction()
