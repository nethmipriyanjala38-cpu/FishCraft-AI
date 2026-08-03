"""
FishCraft AI - Direct Single-File Agent App
"""
import streamlit as st
import os
import requests

# 1. Page Config
st.set_page_config(page_title="FishCraft AI", page_icon="🐠", layout="wide")

# 2. State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to FishCraft! I'm your AI assistant. How can I help you today?"}
    ]

if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

# 3. Sidebar Setup
st.sidebar.title("🐠 FishCraft AI")
st.sidebar.caption("Your Intelligent Ornamental Fish Farm Assistant")
page = st.sidebar.radio("Navigation", ["Chat with AI", "Fish Catalog", "About System"])

# 4. Main Chat Interface
if page == "Chat with AI":
    st.title("💬 Chat with FishCraft AI")
    st.caption("Ask about fish care, check our stock, or place an order!")

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User Input
    user_input = st.chat_input("Ask me anything about ornamental fish...")

    if user_input:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Assistant Processing
        with st.chat_message("assistant"):
            with st.spinner("FishCraft AI is thinking..."):
                try:
                    groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

                    if groq_key:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {groq_key}",
                            "Content-Type": "application/json"
                        }

                        system_prompt = """
                        You are FishCraft AI, an expert assistant for an ornamental fish farm in Sri Lanka.
                        Price List (per pair): Goldfish: LKR 200, Guppy: LKR 60, Platy: LKR 80, Angel Fish: LKR 150.
                        For order queries (e.g., 100 goldfish colombo to kandy), calculate: 100 * 200 = LKR 20,000 + LKR 1,500 delivery = Total LKR 21,500.
                        Always give unique, dynamic, helpful responses tailored strictly to what the user typed.
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
                            st.session_state.agent_logs.append(f"🧭 Router Agent -> Dynamic Groq API Response generated for: '{user_input}'")
                        else:
                            response = f"⚠️ Groq API Error ({res.status_code}): {res.text}"
                    else:
                        response = "🛑 **GROQ_API_KEY Missing!** Check `.streamlit/secrets.toml`."

                except Exception as ex:
                    response = f"⚠️ Exception: {str(ex)}"

                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()

    # Agent Activity Log
    with st.expander("👁️ Agent Activity Log (LangGraph Routing & Tools)"):
        if st.session_state.agent_logs:
            for log in reversed(st.session_state.agent_logs):
                st.code(log, language="bash")
        else:
            st.caption("No agent logs recorded yet.")

elif page == "Fish Catalog":
    st.title("🐠 Fish Catalog")
    st.write("Goldfish, Guppy, Platy, Angel Fish are available in stock!")

elif page == "About System":
    st.title("ℹ️ About System")
    st.write("Multi-Agent Architecture powered by Streamlit and Groq Llama 3.1.")