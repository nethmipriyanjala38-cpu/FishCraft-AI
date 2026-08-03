"""
FishCraft AI - Configuration & Settings
Central configuration for models, fish catalog, and API clients.
"""

import streamlit as st
from openai import OpenAI

# ─── Model Configuration ────────────────────────────────────────────
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Fast model for routing, sales, analytics, QA (Groq - free, ultra-low latency)
GROQ_FAST_MODEL = "llama-3.1-8b-instant"

# Deep reasoning model for fish care expert (OpenRouter - higher quality)
OPENROUTER_DEEP_MODEL = "google/gemini-flash-1.5"

# ─── API Clients ────────────────────────────────────────────────────

def get_groq_client() -> OpenAI:
    """Get OpenAI-compatible client for Groq API."""
    return OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url=GROQ_BASE_URL,
    )

def get_openrouter_client() -> OpenAI:
    """Get OpenAI-compatible client for OpenRouter API."""
    return OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url=OPENROUTER_BASE_URL,
    )

# ─── Fish Catalog ───────────────────────────────────────────────────

FISH_CATALOG = {
    "goldfish": {
        "name": "Goldfish",
        "sinhala_name": "ගෝල්ඩ්ෆිෂ්",
        "price_per_pair": 200,
        "currency": "LKR",
        "stock": 50,
        "emoji": "🐠",
        "description": "Beautiful ornamental goldfish, vibrant orange-gold color. Hardy and beginner-friendly.",
        "care_level": "Easy",
        "tank_size": "60+ liters",
        "water_temp": "18-24°C",
    },
    "guppy": {
        "name": "Guppy",
        "sinhala_name": "ගප්පි",
        "price_per_pair": 60,
        "currency": "LKR",
        "stock": 100,
        "emoji": "🐟",
        "description": "Colorful livebearers with stunning tail patterns. Perfect starter fish.",
        "care_level": "Easy",
        "tank_size": "40+ liters",
        "water_temp": "22-28°C",
    },
    "platy": {
        "name": "Platy",
        "sinhala_name": "ප්ලේටි",
        "price_per_pair": 80,
        "currency": "LKR",
        "stock": 75,
        "emoji": "🐡",
        "description": "Peaceful, colorful livebearers available in many color varieties. Great community fish.",
        "care_level": "Easy",
        "tank_size": "40+ liters",
        "water_temp": "20-26°C",
    },
    "angelfish": {
        "name": "Angelfish",
        "sinhala_name": "එන්ජල්ෆිෂ්",
        "price_per_pair": 150,
        "currency": "LKR",
        "stock": 30,
        "emoji": "👼",
        "description": "Elegant freshwater angels with flowing fins. A centerpiece for any aquarium.",
        "care_level": "Moderate",
        "tank_size": "100+ liters",
        "water_temp": "24-30°C",
    },
}

# ─── RAG Configuration ──────────────────────────────────────────────

KNOWLEDGE_BASE_DIR = "knowledge_base"
CHROMA_COLLECTION_NAME = "fishcraft_knowledge"
CHROMA_PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
RAG_TOP_K = 5

# ─── App Configuration ──────────────────────────────────────────────

APP_NAME = "FishCraft AI"
APP_ICON = "🐠"
APP_TAGLINE = "Your Intelligent Ornamental Fish Farm Assistant"
FARM_LOCATION = "Sri Lanka"
CONTACT_WHATSAPP = "+94 77 123 4567"
CONTACT_EMAIL = "info@fishcraft.lk"
