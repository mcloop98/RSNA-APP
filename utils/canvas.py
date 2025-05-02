# utils/canvas.py
import streamlit as st
from PIL import Image, ImageDraw
import datetime
import gspread
from google.oauth2.service_account import Credentials
import numpy as np
import streamlit_drawable_canvas as sdc


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

    st.markdown("<h3 style='color:white;'>Drag the dot to where you see the dissection flap:</h3>", unsafe_allow_html=True)

    # Define initial draggable dot
    initial_circle = {
        "type": "circle",
        "left": cw // 2,
        "top": ch // 2,
        "radius": 10,
        "fill": "rgba(0, 255, 0, 0.6)",
        "stroke": "green",
        "strokeWidth": 0,
        "originX": "center",
        "originY": "center",
        "hasControls": False,
        "hasBorders": False,
        "selectable": True
    }

    canvas_result = sdc.st_canvas(
        fill_color="rgba(0, 255, 0, 0.3)",
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=ch,
        width=cw,
        drawing_mode="transform",
        key="canvas",
        initial_drawing={"objects": [initial_circle]}
    )

    if canvas_result.json_data and canvas_result.json_data.get("objects"):
        obj = canvas_result.json_data["objects"][0]
        x, y = obj.get("left"), obj.get("top")
        if x is not None and y is not None:
            st.session_state["last_click"] = {"x": x, "y": y}

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
        st.warning("Please drag the dot to your selected location.")
