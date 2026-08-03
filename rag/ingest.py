"""
FishCraft AI - Knowledge Base Ingestion
Loads Markdown documents, chunks them, and stores them in ChromaDB.
"""

import os
import glob
import streamlit as st
import chromadb
from config.settings import (
    KNOWLEDGE_BASE_DIR,
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
from rag.embeddings import get_embedding_function

def simple_text_splitter(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """
    A simple recursive character text splitter.
    Splits by double newline (paragraphs), then single newline, then space if needed,
    ensuring chunks are under chunk_size and have chunk_overlap.
    """
    # For a simple implementation, we'll just split by paragraphs and combine them
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If a single paragraph is larger than chunk size, we need to split it
            if len(para) > chunk_size:
                # Split by words
                words = para.split(' ')
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) < chunk_size:
                        temp_chunk += word + " "
                    else:
                        chunks.append(temp_chunk.strip())
                        # Start new chunk with overlap
                        overlap_start = max(0, len(temp_chunk) - chunk_overlap)
                        temp_chunk = temp_chunk[overlap_start:] + word + " "
                if temp_chunk:
                    current_chunk = temp_chunk
            else:
                current_chunk = para + "\n\n"
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def ensure_knowledge_base_loaded():
    """
    Check if the knowledge base is loaded in ChromaDB.
    If not, read all markdown files, chunk them, and ingest them.
    """
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        
        # Check if collection exists and has documents
        try:
            collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
            if collection.count() > 0:
                print(f"Knowledge base already loaded with {collection.count()} chunks.")
                return True
        except ValueError:
            # Collection doesn't exist, we need to create it
            pass
            
        print("Ingesting knowledge base...")
        embedding_fn = get_embedding_function()
        
        collection = client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            embedding_function=embedding_fn
        )
        
        # Read all markdown files
        md_files = glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, "*.md"))
        
        if not md_files:
            print(f"Warning: No markdown files found in {KNOWLEDGE_BASE_DIR}")
            return False
            
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        chunk_id_counter = 0
        
        for file_path in md_files:
            filename = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            chunks = simple_text_splitter(content, CHUNK_SIZE, CHUNK_OVERLAP)
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({"source": filename, "chunk_index": i})
                all_ids.append(f"{filename}_chunk_{i}")
                chunk_id_counter += 1
                
        # Batch add to ChromaDB (ChromaDB handles batching internally, but we can just pass the lists)
        if all_chunks:
            collection.add(
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            print(f"Successfully ingested {chunk_id_counter} chunks from {len(md_files)} files.")
        
        return True
        
    except Exception as e:
        print(f"Error loading knowledge base: {str(e)}")
        return False
