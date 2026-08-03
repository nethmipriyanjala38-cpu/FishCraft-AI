"""
FishCraft AI - QA Agent
Uses the Reflection pattern to review and polish responses before sending to user.
"""

from config.settings import get_groq_client, GROQ_FAST_MODEL
from agents.state import AgentState, AgentMessage

def qa_node(state: AgentState) -> dict:
    """Review and polish the final response."""
    query = state["user_query"]
    intent = state["intent"]
    specialist_response = state.get("specialist_response", "")
    
    # If it was a general query that skipped specialists, QA handles it directly
    if intent == "general" or not specialist_response:
        system_prompt = """
        You are the friendly customer service representative for FishCraft AI.
        FishCraft is a premium ornamental fish farm in Sri Lanka.
        Answer the user's general greeting or question politely. 
        Keep it brief. We sell Goldfish, Guppies, Platies, and Angelfish.
        """
        try:
            client = get_groq_client()
            response = client.chat.completions.create(
                model=GROQ_FAST_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.5
            )
            final = response.choices[0].message.content
            
            return {
                "current_agent": "qa_agent",
                "final_response": final,
                "qa_passed": True,
                "agent_messages": [AgentMessage("qa_agent", "user", "Handled general query.", "final_delivery").to_dict()]
            }
        except Exception as e:
            return {
                "current_agent": "qa_agent",
                "final_response": f"⚠️ **Authentication Error:** Please add your valid Groq and OpenRouter API keys to `.streamlit/secrets.toml` to use the AI features. *(System details: {str(e)})*",
                "qa_passed": True
            }

    # Otherwise, QA reflects on the specialist response
    system_prompt = f"""
    You are the Quality Assurance Agent for FishCraft AI.
    Your job is to review the drafted response from a specialist agent to the user's query.
    
    User Query: {query}
    Specialist Draft: {specialist_response}
    
    If the draft is good, helpful, and polite, output the exact draft (or slightly polish its formatting).
    If the draft contains error messages or is unhelpful, rewrite it to be a polite apology on behalf of FishCraft.
    DO NOT change the factual content, prices, or numbers in the draft. Just ensure it reads well.
    """
    
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=GROQ_FAST_MODEL,
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            temperature=0.1
        )
        
        final_polished = response.choices[0].message.content
        
        msg = AgentMessage("qa_agent", "user", "QA review passed, delivering final response.", "final_delivery")
        
        return {
            "current_agent": "qa_agent",
            "qa_passed": True,
            "final_response": final_polished,
            "agent_messages": [msg.to_dict()]
        }
        
    except Exception as e:
        # Fallback to unpolished response if QA fails
        msg = AgentMessage("qa_agent", "user", f"QA review bypassed due to error: {e}", "warning")
        final = specialist_response if specialist_response else f"⚠️ **Authentication Error:** Please add your valid Groq and OpenRouter API keys to `.streamlit/secrets.toml` to use the AI features. *(System details: {str(e)})*"
        return {
            "current_agent": "qa_agent",
            "qa_passed": False,
            "qa_feedback": f"Error: {e}",
            "final_response": final,
            "agent_messages": [msg.to_dict()]
        }
