# utils/analysis.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from scipy.ndimage import gaussian_filter

def display_analysis_section():
    st.markdown("<h2 style='color:white;'>Analysis Section</h2>", unsafe_allow_html=True)

    # Connect to Google Sheet
    sheet_url = "https://docs.google.com/spreadsheets/d/1kcfzQ-EHycjFY9JNDRvRgKYPXzoNsb-Ie0qyb709SAs/export?format=csv"
    try:
        df = pd.read_csv(sheet_url, header=0)  # Explicitly set headers

        if not df.empty and "X coordinate" in df.columns and "Y coordinate" in df.columns:
            x_coords = df["X coordinate"].astype(float)
            y_coords = df["Y coordinate"].astype(float)

            # Load the image used as reference for heatmap (example.png)
            image_path = "example.png"
            image = Image.open(image_path).convert("L")  # Grayscale
            width, height = image.size

            # Scale coordinates to match full-size image
            canvas_width, canvas_height = 800, 611  # original canvas display size
            scale_x = width / canvas_width
            scale_y = height / canvas_height
            x_coords *= scale_x
            y_coords *= scale_y

            # Clip coordinates to image bounds
            x_coords = x_coords.clip(0, width - 1)
            y_coords = y_coords.clip(0, height - 1)

            # Create heatmap
            heatmap, yedges, xedges = np.histogram2d(
                y_coords,  # Y-axis
                x_coords,  # X-axis
                bins=[height, width],
                range=[[0, height], [0, width]]
            )

            if heatmap.max() > 0:
                heatmap = gaussian_filter(heatmap, sigma=15)  # Smoother
                heatmap = heatmap / heatmap.max() * 255  # Normalize for high intensity
                heatmap[heatmap < 1] = 0  # Remove low values for visual clarity

            # Plot
            fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
            ax.imshow(image, cmap='gray')
            ax.imshow(heatmap, cmap='inferno', alpha=0.6)

            ax.set_xlim([0, width])
            ax.set_ylim([height, 0])  # Flip Y-axis
            ax.axis('off')
            ax.set_title("User Answer Heatmap", fontsize=20, fontweight='bold')
            st.pyplot(fig)

            # Show bar graph of frequency in Column C
            values = df["Status"]
            counts = values.value_counts()

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            counts.plot(kind='bar', ax=ax2, color='#1E90FF', edgecolor='black')

            ax2.set_xlabel("Status", fontsize=14)
            ax2.set_ylabel("Frequency", fontsize=14)
            ax2.set_title("Frequency of Values in Correct/Incorrect", fontsize=18, fontweight='bold')
            ax2.grid(axis='y', linestyle='--', alpha=0.6)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)

            st.pyplot(fig2)
        else:
            st.warning("The Google Sheet is empty or missing coordinate columns.")
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
