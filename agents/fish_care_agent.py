"""
FishCraft AI - Fish Care Agent
Uses the ReAct pattern and RAG tool to provide expert fish care advice.
Uses OpenRouter deep reasoning model.
"""

from config.settings import get_openrouter_client, OPENROUTER_DEEP_MODEL
from agents.state import AgentState, AgentMessage
from tools.rag_tool import retrieve_fish_knowledge

def fish_care_node(state: AgentState) -> dict:
    """Provide expert fish care advice using RAG and ReAct pattern."""
    query = state["user_query"]
    history = state.get("chat_history", [])
    
    # 1. Action: Retrieve knowledge
    context, sources = retrieve_fish_knowledge(query)
    
    # Format history
    history_str = ""
    for msg in history[-3:]: # Last 3 messages for context
        role = "User" if msg["role"] == "user" else "FishCraft"
        history_str += f"{role}: {msg['content']}\n"
    
    system_prompt = f"""
    You are the Expert Fish Care Agent for FishCraft AI in Sri Lanka.
    Your job is to provide accurate, helpful, and professional advice about ornamental fish.
    
    Use the provided Knowledge Base Context to answer the user's question.
    If the context doesn't contain the exact answer, use your general knowledge but mention that it's general advice.
    Be concise, friendly, and practical. Use bullet points for readability.
    
    KNOWLEDGE BASE CONTEXT:
    {context}
    
    RECENT CHAT HISTORY:
    {history_str}
    
    REASONING TRACE:
    Before answering, briefly write out your reasoning on how the context applies to the user's question. 
    Put this in a <reasoning> block.
    Then, provide your final answer to the customer.
    """
    
    try:
        client = get_openrouter_client()
        response = client.chat.completions.create(
            model=OPENROUTER_DEEP_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3
        )
        
        full_text = response.choices[0].message.content
        
        # Extract reasoning if present
        reasoning = ""
        final_answer = full_text
        if "<reasoning>" in full_text and "</reasoning>" in full_text:
            start = full_text.find("<reasoning>") + 11
            end = full_text.find("</reasoning>")
            reasoning = full_text[start:end].strip()
            final_answer = full_text[end+12:].strip()
            
        msg = AgentMessage(
            sender="fish_care_expert",
            receiver="qa_agent",
            content="Generated care advice based on RAG.",
            message_type="response",
            metadata={"sources_used": len(sources)}
        )
        
        return {
            "current_agent": "fish_care_expert",
            "rag_context": context,
            "rag_sources": sources,
            "specialist_response": final_answer,
            "specialist_reasoning": reasoning,
            "agent_messages": [msg.to_dict()]
        }
        
    except Exception as e:
        print(f"Fish care error: {e}")
        return {
            "current_agent": "fish_care_expert",
            "specialist_response": f"⚠️ **Authentication Error:** Please add a valid OpenRouter API key to `.streamlit/secrets.toml`. *(Details: {str(e)})*",
            "agent_messages": [AgentMessage("fish_care_expert", "qa_agent", f"Error generating response: {e}", "error").to_dict()]
        }
