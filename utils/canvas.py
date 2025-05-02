# utils/canvas.py
import streamlit as st
from PIL import Image, ImageDraw
import datetime
import gspread
from google.oauth2.service_account import Credentials
import numpy as np


def submit_to_google_sheets(data, correct):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1kcfzQ-EHycjFY9JNDRvRgKYPXzoNsb-Ie0qyb709SAs")
    print("Authorized. Trying to open the sheet...")
    print("Sheet opened successfully:", sheet.title)

    try:
        worksheet = sheet.worksheet("Small Arteries")
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Small Arteries", rows=100, cols=5)
        worksheet.append_row(["X", "Y", "Result", "Timestamp", "Case"])

    worksheet.append_row([
        data['x'],
        data['y'],
        "Correct" if correct else "Incorrect",
        data['timestamp'],
        data['case']
    ])
    return True


def display_canvas_section():
    data = st.session_state.get("canvas_data", {})
    if not data:
        st.error("Canvas data not found.")
        return

    cw, ch = data["canvas_width"], data["canvas_height"]
    xmin, xmax, ymin, ymax = data["x_min"], data["x_max"], data["y_min"], data["y_max"]
    case_name = data.get("case_name", "Case 1")

    try:
        image = Image.open("example.png")
        width, height = image.size
    except Exception as e:
        st.error(f"Failed to load image: {e}")
        return

    st.markdown("<h3 style='color:white;'>Click where you see the dissection flap:</h3>", unsafe_allow_html=True)

    clicked_coords = st.image(image, use_column_width=True, output_format="PNG")
    coords = st.session_state.get("clicked_coords")

    if coords:
        x, y = coords
        st.markdown(f"You clicked at: **X = {x}**, **Y = {y}**")

        image_with_dot = image.copy()
        draw = ImageDraw.Draw(image_with_dot)
        r = 5
        draw.ellipse((x - r, y - r, x + r, y + r), fill="red")
        st.image(image_with_dot, caption="You clicked here", use_column_width=True)

        if not st.session_state.get("answer_submitted"):
            if st.button("Submit Answer"):
                correct = xmin <= x <= xmax and ymin <= y <= ymax
                timestamp = datetime.datetime.now().isoformat()

                result_data = {
                    "x": x,
                    "y": y,
                    "timestamp": timestamp,
                    "case": case_name
                }

                if submit_to_google_sheets(result_data, correct):
                    st.session_state["answer_submitted"] = True
                    color = "rgba(0,255,0,0.8)" if correct else "#ff4d4d"
                    message = "✅ Correct!" if correct else "❌ Incorrect."
                    st.markdown(f"""
                        <div style='background-color: {color}; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;'>
                        {message} Recorded.</div>""", unsafe_allow_html=True)
        else:
            st.info("✅ Answer already submitted. Reload the page to try again.")

    else:
        st.warning("Please click on the image to mark the location.")
