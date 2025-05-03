import streamlit as st
from utils.layout import render_header
from utils.canvas import display_canvas_section
from utils.analysis import display_analysis_section

# Ensure 'utils' is treated as a package
import utils

st.set_page_config(
    page_title="Neurovascular Emergencies in Pediatrics",
    page_icon="🧰",
    layout="centered"
)

# Step 1: Initialize state
if 'view_analysis' not in st.session_state:
    st.session_state.view_analysis = False

# Step 2: Auto-trigger analysis section after interaction
if st.session_state.get("go_to_analysis"):
    st.session_state.view_analysis = True

render_header()

# Step 3: Show analysis or canvas based on state
if st.session_state.view_analysis:
    display_analysis_section()
else:
    st.markdown('''
    <div class="subtitle-text">First step: Can you see the dissection flap?</div>
    ''', unsafe_allow_html=True)
    display_canvas_section()
