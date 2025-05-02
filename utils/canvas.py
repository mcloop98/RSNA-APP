# utils/canvas.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import base64
import io
import datetime
import gspread
from google.oauth2.service_account import Credentials


def decode_base64_to_data_url(base64_string):
    return base64_string  # Already in "data:image/...;base64,..." format from the frontend


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

    background_image_url = None
    try:
        background_image_url = decode_base64_to_data_url(data["image_base64"])
    except Exception as e:
        st.warning(f"Background image could not be decoded: {e}")

    st.markdown("<h3 style='color:white;'>Drag the green point to where you see the dissection flap:</h3>", unsafe_allow_html=True)

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

    st.markdown("<div style='position: relative; display: inline-block;'>", unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.3)",
        stroke_width=2,
        background_image=background_image_url,
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
                submitted = st.button("Submit Answer", key="submit_button")
                if submitted:
                    correct = xmin <= x <= xmax and ymin <= y <= ymax
                    timestamp = datetime.datetime.now().isoformat()

                    result = {
                        "x": x,
                        "y": y,
                        "timestamp": timestamp,
                        "case": case_name
                    }

                    if submit_to_google_sheets(result, correct):
                        st.session_state["answer_submitted"] = True
                        color = "rgba(0,255,0,0.8)" if correct else "#ff4d4d"
                        message = "✅ Correct!" if correct else "❌ Incorrect."
                        st.markdown(f"""
                            <div style='position: absolute; bottom: 10px; left: 50%; transform: translate(-50%, 0); 
                            background-color: {color}; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;'>
                            {message} Recorded.</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%); 
                    background-color: rgba(0,0,0,0.7); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;'>
                    ✅ Answer already submitted. Reload the page to try again.</div>
                </div>""", unsafe_allow_html=True)
                return
    else:
        st.markdown("</div>", unsafe_allow_html=True)
        st.warning("Drag the green point to your answer location.")
