import streamlit as st
import os
from ndvi_page import show_ndvi_page  # Import the NDVI page function

# Set page configuration
st.set_page_config(page_title="AgriShield - AI Crop Monitoring", layout="wide")

# Sidebar Navigation
st.sidebar.title("🌾 AgriShield Navigation")
page = st.sidebar.radio("Go to", ["Home", "NDVI Analysis", "Other Features"])

# Define absolute path to the image
image_path = "D:/Hack/farm_banner.jpeg"  # Update with your correct path

# Home Page
if page == "Home":
    st.title("🏡 Welcome to AgriShield")
    st.write("🚜 AI-driven Crop Disease Prediction and Farm Monitoring")

    # Load the banner image safely
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"⚠️ Image not found! Please check the file path: `{image_path}`")

# NDVI Analysis Page
elif page == "NDVI Analysis":
    show_ndvi_page()  # Calls function from `ndvi_page.py`

# Other Features Placeholder (Expand later)
elif page == "Other Features":
    st.title("📌 Other Features")
    st.write("🔜 More functionalities will be added soon!")
