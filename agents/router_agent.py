"""
FishCraft AI - Router Agent
Classifies user intent and routes to the appropriate specialist.
Uses Groq Llama for fast classification.
"""

import json
from config.settings import get_groq_client, GROQ_FAST_MODEL
from agents.state import AgentState, AgentMessage

def router_node(state: AgentState) -> dict:
    """Classify intent and determine next routing step."""
    query = state["user_query"]
    
    system_prompt = """
    You are the Router Agent for FishCraft AI, an ornamental fish farm in Sri Lanka.
    Your job is to classify the user's query into exactly one of these categories:
    
    1. "fish_care": Questions about fish care, breeding, diseases, tank setup, water quality.
    2. "sales": Questions about buying fish, placing an order, prices, shipping.
    3. "analytics": Questions about stock availability or asking for fish recommendations.
    4. "general": Greetings, farm location, contact info, or anything else.
    
    Output ONLY a valid JSON object with a single key "intent".
    Example: {"intent": "fish_care"}
    """
    
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=GROQ_FAST_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        intent = result.get("intent", "general")
        
        # Validate intent
        valid_intents = ["fish_care", "sales", "analytics", "general"]
        if intent not in valid_intents:
            intent = "general"
            
        msg = AgentMessage(
            sender="router",
            receiver=intent,
            content=f"Routing query to {intent} specialist.",
            message_type="routing",
            metadata={"intent": intent}
        )
        
        return {
            "intent": intent,
            "current_agent": "router",
            "agent_messages": [msg.to_dict()]
        }
        
    except Exception as e:
        print(f"Router error: {e}")
        return {
            "intent": "general",
            "current_agent": "router",
            "agent_messages": [AgentMessage("router", "qa_agent", f"Routing failed (API Key missing?): {e}", "error").to_dict()]
        }
