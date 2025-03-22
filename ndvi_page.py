import streamlit as st
import ndvi  # Import NDVI functions

def show_ndvi_page():
    st.title("🌍 NDVI Analysis for Your Farm")

    # User Inputs for Latitude & Longitude
    latitude = st.number_input("Enter Latitude:", format="%.6f")
    longitude = st.number_input("Enter Longitude:", format="%.6f")

    # Button to Fetch NDVI Data
    if st.button("Fetch NDVI Data"):
        if latitude and longitude:
            st.write(f"📍 Location: ({latitude}, {longitude})")
            st.write("⏳ Fetching NDVI data...")

            try:
                results = ndvi.get_ndvi_analysis(latitude, longitude)
                for res in results:
                    st.write(res)
            except Exception as e:
                st.error(f"Error fetching NDVI: {e}")
