"""
FishCraft AI - RAG Tool
Exposes the retriever to the agents.
"""

from rag.retriever import retrieve_knowledge

def retrieve_fish_knowledge(query: str) -> tuple[str, list[str]]:
    """
    Retrieve knowledge from the RAG pipeline and format it as context.
    
    Returns:
        tuple containing:
        - Formatted context string
        - List of source document names
    """
    results = retrieve_knowledge(query)
    
    if not results:
        return "No relevant information found in the knowledge base.", []
        
    context_parts = []
    sources = set()
    
    for i, res in enumerate(results):
        source = res['source']
        sources.add(source)
        content = res['content']
        context_parts.append(f"[Source: {source}]\n{content}\n")
        
    formatted_context = "\n".join(context_parts)
    return formatted_context, list(sources)
