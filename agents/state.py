"""
FishCraft AI - Shared Agent State
Defines the TypedDict state schema used by all agents in the LangGraph pipeline.
Agent-to-agent communication happens through structured AgentMessage objects.
"""

from typing import TypedDict, List, Dict, Any, Annotated
from datetime import datetime
import operator


class AgentMessage:
    """Structured message for agent-to-agent communication.
    
    This implements a custom communication protocol where agents exchange
    typed messages with metadata, enabling traceable multi-agent collaboration.
    """
    def __init__(
        self,
        sender: str,
        receiver: str,
        content: str,
        message_type: str = "info",  # query, response, review, feedback, routing
        metadata: Dict[str, Any] = None,
    ):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return f"AgentMessage({self.sender} → {self.receiver}: {self.message_type})"


def merge_agent_messages(left: List[dict], right: List[dict]) -> List[dict]:
    """Reducer that appends new agent messages to existing list."""
    return left + right


class AgentState(TypedDict):
    """Shared state flowing through the LangGraph pipeline.
    
    All agents read from and write to this state, enabling
    structured agent-to-agent communication via the agent_messages list.
    """
    # ── User interaction ──
    user_query: str                                          # Current user question
    chat_history: List[dict]                                 # Full conversation history

    # ── Routing ──
    intent: str                                              # Classified intent: fish_care | sales | analytics | general
    current_agent: str                                       # Name of the currently active agent

    # ── RAG context ──
    rag_context: str                                         # Retrieved knowledge chunks
    rag_sources: List[str]                                   # Source document names

    # ── Agent-to-agent communication ──
    agent_messages: Annotated[List[dict], merge_agent_messages]  # Structured inter-agent messages

    # ── Specialist output ──
    specialist_response: str                                 # Response from specialist agent
    specialist_reasoning: str                                # Reasoning trace (ReAct / Planning)

    # ── Order data (sales agent) ──
    order_data: Dict[str, Any]                               # Order details: items, quantities, total

    # ── QA review ──
    qa_passed: bool                                          # Whether QA agent approved the response
    qa_feedback: str                                         # QA agent's review comments

    # ── Final output ──
    final_response: str                                      # Polished response sent to user


def create_initial_state(user_query: str, chat_history: List[dict] = None) -> AgentState:
    """Create a fresh state for a new user query."""
    return {
        "user_query": user_query,
        "chat_history": chat_history or [],
        "intent": "",
        "current_agent": "router",
        "rag_context": "",
        "rag_sources": [],
        "agent_messages": [],
        "specialist_response": "",
        "specialist_reasoning": "",
        "order_data": {},
        "qa_passed": False,
        "qa_feedback": "",
        "final_response": "",
    }
