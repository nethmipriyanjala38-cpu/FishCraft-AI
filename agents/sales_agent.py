"""
FishCraft AI - Sales Agent
Uses the Planning pattern to process orders and calculate prices.
Uses Groq Llama for fast structured output.
"""

import json
from config.settings import get_groq_client, GROQ_FAST_MODEL, FISH_CATALOG
from agents.state import AgentState, AgentMessage
from tools.price_calculator import calculate_order_price
from tools.stock_checker import check_stock
from tools.order_builder import build_order_summary

def sales_node(state: AgentState) -> dict:
    """Process order requests using planning pattern."""
    query = state["user_query"]
    
    # Provide catalog context to the LLM
    catalog_str = "\n".join([f"- {k}: {v['name']} (Rs.{v['price_per_pair']}/pair)" for k, v in FISH_CATALOG.items()])
    
    system_prompt = f"""
    You are the Sales Agent for FishCraft AI.
    Your job is to parse the user's order request into structured JSON data.
    
    AVAILABLE FISH CATALOG:
    {catalog_str}
    
    Identify the fish types and quantities the user wants to buy. 
    IMPORTANT: Our prices are per PAIR. If a user asks for "10 goldfish", that means 5 pairs. If they ask for "10 pairs", that is 10 pairs. Always convert to PAIRS.
    Also identify their delivery location if mentioned (e.g., Colombo, Kandy, Galle).
    If they ask for general prices, just output an empty items dict.
    
    Output ONLY a valid JSON object in this format:
    {{
        "is_order": true/false,
        "items": {{"goldfish": 5, "guppy": 2}}, 
        "location": "colombo",
        "reasoning": "User asked for 10 goldfish (5 pairs) and 2 pairs of guppies to Colombo."
    }}
    Note: Items keys MUST match the catalog keys exactly (goldfish, guppy, platy, angelfish).
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
        
        parsed = json.loads(response.choices[0].message.content)
        is_order = parsed.get("is_order", False)
        items = parsed.get("items", {})
        location = parsed.get("location", "")
        reasoning = parsed.get("reasoning", "")
        
        if is_order and items or "price" in query.lower() or "price" in reasoning.lower():
            # Plan step 2 & 3: Check stock and Calculate prices
            order_data = calculate_order_price(items, location)
            
            # Plan step 4: Build summary
            summary = build_order_summary(order_data)
            
            final_response = "Here is your order summary based on your request:\n\n" + summary + "\n\nWould you like to confirm this order via WhatsApp?"
            
            msg = AgentMessage("sales_agent", "qa_agent", "Processed order calculation.", "response", {"total": order_data.get("total", 0)})
            
            return {
                "current_agent": "sales_agent",
                "specialist_response": final_response,
                "specialist_reasoning": reasoning,
                "order_data": order_data,
                "agent_messages": [msg.to_dict()]
            }
        else:
            # Just asking about sales generally
            general_response = f"Welcome to FishCraft Sales! We offer:\n{catalog_str}\n\nWe offer a 10% discount on orders of 10 or more pairs. Standard shipping is Rs.350 in Colombo. What would you like to order?"
            
            msg = AgentMessage("sales_agent", "qa_agent", "Handled general sales inquiry.", "response")
            
            return {
                "current_agent": "sales_agent",
                "specialist_response": general_response,
                "specialist_reasoning": "User asked a general sales question, not a specific order.",
                "agent_messages": [msg.to_dict()]
            }
            
    except Exception as e:
        print(f"Sales error: {e}")
        return {
            "current_agent": "sales_agent",
            "specialist_response": f"⚠️ **Authentication Error:** Please add a valid Groq API key to `.streamlit/secrets.toml`. *(Details: {str(e)})*",
            "agent_messages": [AgentMessage("sales_agent", "qa_agent", f"Error: {e}", "error").to_dict()]
        }
