"""
FishCraft AI - Sidebar
Renders the navigation and info sidebar.
"""

import streamlit as st
from config.settings import APP_NAME, APP_ICON, APP_TAGLINE, CONTACT_WHATSAPP, CONTACT_EMAIL

def render_sidebar():
    """Renders the sidebar and returns the selected page."""
    with st.sidebar:
        st.title(f"{APP_ICON} {APP_NAME}")
        st.markdown(f"*{APP_TAGLINE}*")
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Go to",
            ["Chat with AI", "Fish Catalog", "About System"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Contact Info
        st.subheader("Contact Us")
        st.markdown(f"""
        <div style="font-size: 0.9rem; color: #a0aec0;">
            <b>WhatsApp:</b> <br/>{CONTACT_WHATSAPP}<br/><br/>
            <b>Email:</b> <br/>{CONTACT_EMAIL}<br/><br/>
            <b>Location:</b> <br/>Colombo, Sri Lanka
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Agent Activity Debugger
        with st.expander("🤖 Agent Activity Log", expanded=False):
            if "last_state" in st.session_state and st.session_state.last_state:
                state = st.session_state.last_state
                msgs = state.get("agent_messages", [])
                
                if msgs:
                    for m in msgs:
                        sender = m.get('sender', 'unknown').replace('_', ' ').title()
                        receiver = m.get('receiver', 'unknown').replace('_', ' ').title()
                        type_color = {
                            "routing": "blue",
                            "response": "green",
                            "review": "orange",
                            "final_delivery": "violet",
                            "error": "red"
                        }.get(m.get('message_type', 'info'), "gray")
                        
                        st.markdown(f"""
                        <div style="font-size: 0.75rem; border-left: 2px solid {type_color}; padding-left: 5px; margin-bottom: 8px;">
                            <b>{sender}</b> → <b>{receiver}</b><br/>
                            <span style="color: #cbd5e1;">{m.get('content', '')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No agent activity yet.")
            else:
                st.caption("No agent activity yet.")
                
        # Clear Chat Button
        st.divider()
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_state = None
            st.rerun()
            
    # Map friendly names to page codes
    page_map = {
        "Chat with AI": "chat",
        "Fish Catalog": "catalog",
        "About System": "about"
    }
    
    return page_map[page]
