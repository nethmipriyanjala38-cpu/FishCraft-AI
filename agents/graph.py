"""
FishCraft AI - LangGraph Orchestration
Connects all agents into a directed graph.
"""

from langgraph.graph import StateGraph, END
from agents.state import AgentState, create_initial_state
from agents.router_agent import router_node
from agents.fish_care_agent import fish_care_node
from agents.sales_agent import sales_node
from agents.analytics_agent import analytics_node
from agents.qa_agent import qa_node

def route_from_router(state: AgentState):
    """Conditional edge routing logic based on router classification."""
    intent = state.get("intent", "general")
    if intent == "fish_care":
        return "fish_care"
    elif intent == "sales":
        return "sales"
    elif intent == "analytics":
        return "analytics"
    else:
        return "qa" # General queries skip specialists and go to QA

def create_fishcraft_graph():
    """Build and compile the LangGraph for the multi-agent system."""
    
    # Initialize graph
    workflow = StateGraph(AgentState)
    
    # Add nodes (agents)
    workflow.add_node("router", router_node)
    workflow.add_node("fish_care", fish_care_node)
    workflow.add_node("sales", sales_node)
    workflow.add_node("analytics", analytics_node)
    workflow.add_node("qa", qa_node)
    
    # Add edges
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        route_from_router,
        {
            "fish_care": "fish_care",
            "sales": "sales",
            "analytics": "analytics",
            "qa": "qa"
        }
    )
    
    # All specialist paths converge at QA
    workflow.add_edge("fish_care", "qa")
    workflow.add_edge("sales", "qa")
    workflow.add_edge("analytics", "qa")
    
    # QA ends the graph
    workflow.add_edge("qa", END)
    
    # Compile
    return workflow.compile()

def run_agent_pipeline(user_query: str, chat_history: list = None) -> dict:
    """Convenience function to run the graph and return the final state."""
    graph = create_fishcraft_graph()
    initial_state = create_initial_state(user_query, chat_history)
    
    # Run the graph synchronously
    # The output is a dict representing the final state or state updates
    final_state = graph.invoke(initial_state)
    
    return final_state
