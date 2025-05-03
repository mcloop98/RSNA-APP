# utils/analysis.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

def display_analysis_section():
    st.markdown("<h2 style='color:white;'>Analysis Section</h2>", unsafe_allow_html=True)

    sheet_url = "https://docs.google.com/spreadsheets/d/1kcfzQ-EHycjFY9JNDRvRgKYPXzoNsb-Ie0qyb709SAs/export?format=csv"
    try:
        df = pd.read_csv(sheet_url, header=0)

        if not df.empty and "X coordinate" in df.columns and "Y coordinate" in df.columns:
            x_coords = df["X coordinate"].astype(float)
            y_coords = df["Y coordinate"].astype(float)

            image_path = "example.png"
            image = Image.open(image_path).convert("L")
            width, height = image.size

            x_coords = x_coords.clip(0, width - 1)
            y_coords = y_coords.clip(0, height - 1)

            heatmap, yedges, xedges = np.histogram2d(
                y_coords,
                x_coords,
                bins=[height, width],
                range=[[0, height], [0, width]]
            )

            if heatmap.max() > 0:
                heatmap = gaussian_filter(heatmap, sigma=15)
                heatmap = heatmap / heatmap.max() * 255
                heatmap[heatmap < 1] = 0

            fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
            ax.imshow(image, cmap='gray')
            ax.imshow(heatmap, cmap='inferno', alpha=0.6)

            ax.set_xlim([0, width])
            ax.set_ylim([height, 0])
            ax.axis('off')
            ax.set_title("User Answer Heatmap", fontsize=20, fontweight='bold')
            st.pyplot(fig)

            if "Status" in df.columns:
                values = df["Status"]
                counts = values.value_counts()

                fig2, ax2 = plt.subplots(figsize=(10, 6))
                counts.plot(kind='bar', ax=ax2, color='#1E90FF', edgecolor='black')

                ax2.set_xlabel("Status", fontsize=14, fontweight='bold')
                ax2.set_ylabel("Frequency", fontsize=14)
                ax2.set_title("Frequency of Values in Correct/Incorrect", fontsize=18, fontweight='bold')
                ax2.grid(axis='y', linestyle='--', alpha=0.6)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.tick_params(axis='x', labelrotation=0)
                st.pyplot(fig2)
            else:
                st.warning("Missing 'Status' column for bar chart.")

            if "Letter" in df.columns:
                letter_counts = df["Letter"].value_counts().sort_index()
                fig3, ax3 = plt.subplots(figsize=(10, 6))
                letter_counts.plot(kind='bar', ax=ax3, color='orange', edgecolor='black')
                ax3.set_xlabel("Letter", fontsize=14, fontweight='bold')
                ax3.set_ylabel("Frequency", fontsize=14)
                ax3.set_title("Marked Letters", fontsize=18, fontweight='bold')
                ax3.tick_params(axis='x', rotation=0, labelsize=12)
                ax3.grid(axis='y', linestyle='--', alpha=0.6)
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                st.pyplot(fig3)
            else:
                st.warning("Missing 'Letter' column for bar chart.")

        else:
            st.warning("The Google Sheet is empty or missing coordinate columns.")
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
