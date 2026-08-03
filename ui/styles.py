"""
FishCraft AI - UI Styles
Injects premium CSS for a dark-themed, glassmorphic UI.
"""

import streamlit as st

def inject_custom_css():
    """Injects comprehensive custom CSS for a stunning FishCraft UI."""
    css = """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Dark Theme Background */
        .stApp {
            background-color: #050b14;
            background-image: 
                radial-gradient(at 0% 0%, rgba(2, 62, 138, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(0, 212, 170, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: #e0e6ed;
        }
        
        /* Typography */
        h1, h2, h3, h4 {
            color: #ffffff;
            font-weight: 600;
        }
        
        h1 {
            background: linear-gradient(90deg, #00d4aa, #00b4d8, #023e8a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            margin-bottom: 20px;
        }
        
        /* Chat Interface Styles */
        .stChatMessage {
            background-color: transparent !important;
            padding: 1rem 0 !important;
        }
        
        /* Bot Message styling */
        [data-testid="stChatMessage"][data-baseweb="block"]:has([data-testid="stChatMessageAvatarUser"]) {
            /* User Message wrapper */
        }
        
        /* Bubble styling */
        .chat-bubble {
            padding: 1.2rem;
            border-radius: 16px;
            margin-bottom: 10px;
            line-height: 1.5;
            animation: fadeIn 0.3s ease-in-out;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .chat-bubble-user {
            background: linear-gradient(135deg, rgba(0, 180, 216, 0.2), rgba(2, 62, 138, 0.3));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-top-right-radius: 4px;
            border-left: 3px solid #00b4d8;
            margin-left: 10%;
        }
        
        .chat-bubble-bot {
            background: rgba(15, 25, 40, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-top-left-radius: 4px;
            border-left: 3px solid #00d4aa;
            margin-right: 10%;
        }
        
        /* Expander (Agent Reasoning/Logs) */
        .streamlit-expanderHeader {
            background-color: rgba(20, 30, 50, 0.5) !important;
            border-radius: 8px !important;
            color: #a0aec0 !important;
            font-size: 0.9rem !important;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .streamlit-expanderContent {
            background-color: rgba(10, 15, 25, 0.5) !important;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            border-left: 1px solid rgba(255, 255, 255, 0.05);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
            color: #cbd5e1;
            padding: 1rem !important;
        }
        
        /* Chat Input */
        .stChatInputContainer {
            padding-bottom: 2rem !important;
            background-color: transparent !important;
        }
        
        [data-testid="stChatInput"] {
            border-radius: 20px !important;
            background-color: rgba(15, 25, 40, 0.7) !important;
            border: 1px solid rgba(0, 212, 170, 0.3) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.1) !important;
        }
        
        [data-testid="stChatInput"] textarea {
            color: white !important;
        }
        
        [data-testid="stChatInput"] button {
            color: #00d4aa !important;
            background: rgba(0, 212, 170, 0.1) !important;
            border-radius: 50% !important;
        }
        
        [data-testid="stChatInput"] button:hover {
            background: rgba(0, 212, 170, 0.2) !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 12, 22, 0.9) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(90deg, rgba(0, 180, 216, 0.1), rgba(0, 212, 170, 0.1));
            border: 1px solid rgba(0, 212, 170, 0.3);
            color: #00d4aa;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton button:hover {
            background: linear-gradient(90deg, rgba(0, 180, 216, 0.2), rgba(0, 212, 170, 0.2));
            border-color: #00d4aa;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.15);
            color: white;
        }
        
        /* Product Cards */
        .fish-card {
            background: rgba(15, 25, 40, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .fish-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, #00d4aa, #00b4d8);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .fish-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border-color: rgba(0, 212, 170, 0.2);
        }
        
        .fish-card:hover::before {
            opacity: 1;
        }
        
        .fish-emoji-bg {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            display: inline-block;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
            transition: transform 0.3s ease;
        }
        
        .fish-card:hover .fish-emoji-bg {
            transform: scale(1.1) rotate(-5deg);
        }
        
        .fish-price {
            font-size: 1.25rem;
            color: #00d4aa;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        
        .fish-stock {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            background: rgba(0, 212, 170, 0.1);
            color: #00d4aa;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        
        .fish-detail {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-bottom: 0.2rem;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.2rem;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 212, 170, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 212, 170, 0.5);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
