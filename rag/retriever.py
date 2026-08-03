"""
FishCraft AI - Knowledge Retriever
Queries ChromaDB to retrieve relevant chunks for a given query.
"""

import chromadb
from config.settings import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    RAG_TOP_K
)
from rag.embeddings import get_embedding_function

def retrieve_knowledge(query: str, top_k: int = RAG_TOP_K) -> list[dict]:
    """
    Retrieve the most relevant knowledge chunks for a given query.
    
    Args:
        query: The user's question or search terms
        top_k: Number of chunks to retrieve
        
    Returns:
        List of dictionaries containing 'content', 'source', and 'score'
    """
    try:
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        embedding_fn = get_embedding_function()
        
        try:
            collection = client.get_collection(
                name=CHROMA_COLLECTION_NAME,
                embedding_function=embedding_fn
            )
        except ValueError:
            # Collection doesn't exist
            return []
            
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        formatted_results = []
        if results and 'documents' in results and results['documents']:
            docs = results['documents'][0]
            metadatas = results['metadatas'][0] if 'metadatas' in results else [{}] * len(docs)
            distances = results['distances'][0] if 'distances' in results else [0.0] * len(docs)
            
            for doc, meta, dist in zip(docs, metadatas, distances):
                formatted_results.append({
                    "content": doc,
                    "source": meta.get("source", "Unknown"),
                    "score": dist  # Note: lower distance means higher similarity (usually L2)
                })
                
        return formatted_results
        
    except Exception as e:
        print(f"Error retrieving knowledge: {str(e)}")
        return []
