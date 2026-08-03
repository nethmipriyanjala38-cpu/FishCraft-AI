"""
FishCraft AI - Fish Catalog UI
Renders the visual fish catalog using data from config.
"""

import streamlit as st
from config.settings import FISH_CATALOG

def render_fish_catalog():
    """Render a beautiful grid of fish products."""
    st.markdown("<h1>🐟 FishCraft Collection</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;'>Browse our premium ornamental fish, bred and raised in optimal tropical conditions in Sri Lanka.</p>", unsafe_allow_html=True)
    
    # Create columns for grid (2 items per row)
    cols = st.columns(2)
    
    for i, (key, data) in enumerate(FISH_CATALOG.items()):
        # Alternate columns
        col = cols[i % 2]
        
        with col:
            # Render card using HTML/CSS
            card_html = f"""
            <div class="fish-card">
                <div class="fish-emoji-bg">{data['emoji']}</div>
                <h3>{data['name']} <span style="font-size: 0.9rem; color: #64748b; font-weight: 400;">({data['sinhala_name']})</span></h3>
                <div class="fish-price">Rs. {data['price_per_pair']} <span style="font-size: 0.8rem; color: #64748b; font-weight: 400;">/ pair</span></div>
                <div class="fish-stock">Stock: {data['stock']} pairs</div>
                
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 1rem; min-height: 45px;">
                    {data['description']}
                </p>
                
                <div class="fish-detail"><span>Care Level</span> <span>{data['care_level']}</span></div>
                <div class="fish-detail"><span>Min. Tank</span> <span>{data['tank_size']}</span></div>
                <div class="fish-detail"><span>Temp</span> <span>{data['water_temp']}</span></div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Action button
            if st.button(f"Ask AI about {data['name']}", key=f"btn_{key}"):
                # Set a flag to switch to chat and prefill query
                st.session_state.prefill_query = f"I'm interested in buying {data['name']}. What do I need to know?"
                st.session_state.force_page = "chat"
                st.rerun()
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Discount banner
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(0, 212, 170, 0.1), rgba(0, 180, 216, 0.1)); 
                border-left: 4px solid #00d4aa; padding: 1.5rem; border-radius: 8px;">
        <h4 style="margin-top: 0; color: #00d4aa;">🎉 Bulk Discount Available</h4>
        <p style="margin-bottom: 0;">Order 10 or more pairs (any combination) and receive a <strong>10% discount</strong> on your total order. Our Sales Agent will apply this automatically!</p>
    </div>
    """, unsafe_allow_html=True)
