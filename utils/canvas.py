import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


def display_canvas_section():
    st.markdown("<h3 style='color:white;'>Example: Which letter is closest to the location of the dissection flap?</h3>", unsafe_allow_html=True)

    # Load the image
    img = Image.open("example.png")

    st.image(img, caption="Example Case Image")

    # Google Sheets setup
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1kcfzQ-EHycjFY9JNDRvRgKYPXzoNsb-Ie0qyb709SAs/edit#gid=0")
    worksheet = sheet.worksheet("Small Arteries")

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
