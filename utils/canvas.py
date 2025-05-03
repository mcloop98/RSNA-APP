import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


def display_canvas_section():
    st.markdown("<h3 style='color:white;'>Example: Which letter is closest to the location of the dissection flap?</h3>", unsafe_allow_html=True)

    # Load the image
    img = Image.open("example.png")
    img_with_buttons = img.copy()
    draw = ImageDraw.Draw(img_with_buttons)

    # Button definitions: label -> (x, y)
    button_positions = {
        "A": (1073, 945),
        "B": (1171, 629),
        "C": (619, 633),
        "D": (935, 523),
        "E": (1307, 411),
        "F": (1482, 133),
        "G": (272, 591)
    }

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        font = ImageFont.load_default()

    # Draw each letter on the image
    for letter, (x, y) in button_positions.items():
        bbox = font.getbbox(letter)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = (x - text_width // 2, y - text_height // 2 - bbox[1])
        draw.text(text_position, letter, fill="red", font=font)

    st.image(img_with_buttons, caption="Example Case Image with Buttons")

    # Google Sheets setup
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1kcfzQ-EHycjFY9JNDRvRgKYPXzoNsb-Ie0qyb709SAs/edit#gid=0")
    worksheet = sheet.worksheet("Small Arteries")

    # Render buttons horizontally
    cols = st.columns(len(button_positions))
    for idx, (letter, (x, y)) in enumerate(button_positions.items()):
        if cols[idx].button(letter):
            status = "Correct" if letter == "C" else "Incorrect"
            timestamp = datetime.now().isoformat()
            case = "Case 1"
            worksheet.append_row([x, y, status, timestamp, case, letter])
            if status == "Correct":
                st.markdown(f"""
                <div style='background-color:#28a745; padding:10px; border-radius:8px; text-align:center; color:white; font-size:18px; font-weight:bold;'>
                    ✅ {status}, {case}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background-color:#dc3545; padding:10px; border-radius:8px; text-align:center; color:white; font-size:18px; font-weight:bold;'>
                    ❌ {status}, {case}
                </div>
                """, unsafe_allow_html=True)
