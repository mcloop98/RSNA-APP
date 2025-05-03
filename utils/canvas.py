import streamlit as st
from PIL import Image

def display_canvas_section():
    st.markdown("<h3 style='color:white;'>Example: Where would the dissection flap be?</h3>", unsafe_allow_html=True)

    st.image("example.png", caption="Example Case Image", use_column_width=True)
