"""
FishCraft AI - Chat Interface Component
Direct Integration with Groq API
"""

import streamlit as st
import os
import requests

def render_chat_interface():
    st.title("💬 Chat with FishCraft AI")
    st.caption("Ask about fish care, check our stock, or place an order!")

    # 1. Session state initializations
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to FishCraft! I'm your AI assistant. I can help you with expert fish care advice, check our current stock, or take your order. How can I help you today?"}
        ]

    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []

    # 2. Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 3. Handle Chat Input
    user_input = st.chat_input("Ask me anything about ornamental fish...")

    if user_input:
        # User message append
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Immediate display
        with st.chat_message("user"):
            st.write(user_input)

        # AI Agent Response Generation
        with st.chat_message("assistant"):
            with st.spinner("FishCraft AI Agent is thinking..."):
                try:
                    # Get Groq API key
                    groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

                    if groq_key:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {groq_key}",
                            "Content-Type": "application/json"
                        }

                        system_prompt = """
                        You are FishCraft AI, an intelligent assistant for an ornamental fish farm in Sri Lanka.
                        
                        Our Price List (per pair):
                        - Goldfish (ගොල්ෆිශ්): LKR 200
                        - Guppy (සරිගප්පි): LKR 60[cite: 1]
                        - Platy (ප්ලේටි): LKR 80[cite: 1]
                        - Angel Fish (එන්ජල්): LKR 150[cite: 1]

                        If user asks for order calculations or transport (e.g., 100 goldfish colombo to kandy):
                        Calculate: 100 pairs * LKR 200 = LKR 20,000 + LKR 1,500 delivery fee = Total LKR 21,500.

                        If user says 'Hey' or greetings, welcome them warmly and mention what you can do.
                        Always give helpful, dynamic, non-repetitive answers tailored specifically to what the user typed.
                        """

                        payload = {
                            "model": "llama-3.1-8b-instant",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_input}
                            ],
                            "temperature": 0.3
                        }

                        res = requests.post(url, headers=headers, json=payload)

                        if res.status_code == 200:
                            response = res.json()["choices"][0]["message"]["content"]
                            st.session_state.agent_logs.append(f"🧭 Router Agent ➔ Query '{user_input}' routed to Groq Llama-3.1-8B.")
                        else:
                            response = f"⚠️ Groq API Error ({res.status_code}): {res.text}"
                    else:
                        response = "🛑 **GROQ_API_KEY Missing!** Please check your `.streamlit/secrets.toml` file."

                except Exception as ex:
                    response = f"⚠️ System Exception: {str(ex)}"

                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()

    # 4. Agent Activity Log Visualizer
    with st.expander("👁️ Agent Activity Log (LangGraph Routing & Tools)"):
        if st.session_state.agent_logs:
            for log in reversed(st.session_state.agent_logs):
                st.code(log, language="bash")
        else:
            st.caption("No active agent execution recorded yet.")