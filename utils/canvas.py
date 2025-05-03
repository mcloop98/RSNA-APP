import streamlit as st
from PIL import Image, ImageDraw

def display_canvas_section():
    st.markdown("<h3 style='color:white;'>Example: Where would the dissection flap be?</h3>", unsafe_allow_html=True)

    # Load the image
    img = Image.open("example.png")
    
    # Create a copy of the image to draw on
    img_with_button = img.copy()
    draw = ImageDraw.Draw(img_with_button)
    
    # Define button properties
    button_radius = 20
    button_position = (img.width // 2, img.height // 2)  # Center of the image
    
    # Draw a red circle
    draw.ellipse([
        button_position[0] - button_radius,
        button_position[1] - button_radius,
        button_position[0] + button_radius,
        button_position[1] + button_radius
    ], fill='red')
    
    # Display the image with the button
    st.image(img_with_button, caption="Example Case Image with Button")
