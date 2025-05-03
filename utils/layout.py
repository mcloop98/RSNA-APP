# utils/layout.py
import streamlit as st
import base64
import io
from PIL import Image

def render_header():
    st.markdown("""
<style>
.stApp {
    background: black;
    text-align: center;
}
.logo-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
}
.logo-row img {
    height: 80px;
}
.title-text {
    font-size: 32px;
    color: yellow;
    font-weight: bold;
    margin: 10px 0;
}
.subtitle-text {
    font-size: 26px;
    color: white;
    margin: 20px auto 30px;
    font-weight: bold;
    background: #1E90FF;
    padding: 10px 20px;
    border-radius: 8px;
    display: inline-block;
}
.canvas-wrapper,
.button-row {
    margin: 0 auto;
    max-width: 800px;
    padding: 20px;
    display: flex;
    justify-content: center;
    gap: 30px;
}
#r {
    margin-top: 8px;
}
/* Style for orange and green buttons */
.stButton > button {
    background-color: #FFA500;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #FF8C00;
}
.bullet-box {
    background-color: #2E8B57;
    color: white;
    text-align: left;
    padding: 20px;
    margin: 20px auto;
    max-width: 800px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

    # Load and encode images
    encoded_imgs = []
    for file in ["rsna.png", "ut.png", "example.png"]:
        with open(file, "rb") as f:
            img_data = f.read()
            if file == "example.png":
                img = Image.open(io.BytesIO(img_data)).convert("RGB")
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                img_data = buf.getvalue()
            encoded_imgs.append(f"data:image/png;base64,{base64.b64encode(img_data).decode()}")

    st.markdown(f'''
<div class="logo-row">
    <img src="{encoded_imgs[0]}">
    <img src="{encoded_imgs[1]}">
</div>
<div class="title-text">Small Arteries, Big Challenges:<br>Neurovascular Emergencies in Pediatrics</div>
''', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Home", key="home_button"):
            st.session_state.view_analysis = False
    with col2:
        if st.button("Analysis of Answers", key="header_button"):
            st.session_state.view_analysis = True

    st.markdown('''
<div class="bullet-box">
    <strong>This is a sample of the app:</strong>
    <ul>
        <li>Step-by-step guidance through cases.</li>
<li>Click to view detailed analysis and heat maps.</li>
<li>Tested by residents and fellows.</li>
<li>Key confusion points will inform educational highlights.</li>
<li>Showcased at the upcoming conference.</li>
    </ul>
</div>
''', unsafe_allow_html=True)

    # Set canvas dimensions
    img = Image.open("example.png").convert("RGB")
    w, h = img.size
    cw, ch = 800, int(800 * h / w)
    sx, sy = 800 / w, ch / h

    st.session_state.canvas_data = {
        "image_base64": encoded_imgs[2],
        "canvas_width": cw,
        "canvas_height": ch,
        "x_min": 517 * sx,
        "x_max": 760 * sx,
        "y_min": 557 * sy,
        "y_max": 624 * sy
    }
