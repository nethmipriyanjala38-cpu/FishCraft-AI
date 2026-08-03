"""
FishCraft AI - Analytics Agent
Handles stock inquiries and fish recommendations using tool-use pattern.
"""

from config.settings import get_groq_client, GROQ_FAST_MODEL
from agents.state import AgentState, AgentMessage
from tools.stock_checker import check_stock

def analytics_node(state: AgentState) -> dict:
    """Provide stock info and recommendations."""
    query = state["user_query"]
    
    # 1. Action: Use tool to get stock
    stock_data = check_stock()
    
    stock_str = ""
    for k, v in stock_data.items():
        stock_str += f"- {v['name']}: {v['stock']} pairs available ({v['status']})\n"
        
    system_prompt = f"""
    You are the Analytics & Recommendations Agent for FishCraft AI.
    Your job is to answer questions about stock availability or recommend fish to the user.
    
    CURRENT STOCK DATA:
    {stock_str}
    
    If they ask about stock, use the data above.
    If they want recommendations, recommend from our catalog (Goldfish, Guppy, Platy, Angelfish).
    - Beginners/Small tanks: Guppy, Platy
    - Medium tanks/Peaceful: Guppy, Platy, Goldfish (needs bigger tank though)
    - Large tanks/Centerpiece: Angelfish
    
    Be helpful and concise.
    """
    
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=GROQ_FAST_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3
        )
        
        final_answer = response.choices[0].message.content
        
        msg = AgentMessage("analytics_agent", "qa_agent", "Provided stock/recommendation data.", "response")
        
        return {
            "current_agent": "analytics_agent",
            "specialist_response": final_answer,
            "agent_messages": [msg.to_dict()]
        }
        
    except Exception as e:
        return {
            "current_agent": "analytics_agent",
            "specialist_response": f"⚠️ **Authentication Error:** Please add a valid Groq API key to `.streamlit/secrets.toml`. *(Details: {str(e)})*",
            "agent_messages": [AgentMessage("analytics_agent", "qa_agent", f"Error: {e}", "error").to_dict()]
        }
