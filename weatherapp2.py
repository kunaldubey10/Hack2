import streamlit as st
import os
import requests
from datetime import datetime
from ndvi_page import show_ndvi_page  # Import NDVI Analysis Page

# Set page configuration
st.set_page_config(page_title="AgriShield - AI Crop Monitoring", layout="wide")

# Sidebar Navigation
st.sidebar.title("🌾 AgriShield Navigation")
page = st.sidebar.radio("Go to", ["Home", "NDVI Analysis", "Leaf Disease Detection", "Chatbot", "Other Features"])

# Define absolute path to the image
image_path = "D:/Hack/farm_banner.jpeg"

# OpenWeather API Key (Replace with your own key)
API_KEY = "e15e7551cdb8ed7df8c7fd1833af7fec"
DEFAULT_CITY = "Delhi"
DEFAULT_LAT, DEFAULT_LON = 28.7041, 77.1025  # Default location (Delhi, India)

# Function to fetch live weather data
def get_weather(city=DEFAULT_CITY, lat=DEFAULT_LAT, lon=DEFAULT_LON):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "City": city,
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"],
            "Condition": data["weather"][0]["description"],
            "Rain": data.get("rain", {}).get("1h", 0),  # Rainfall in last 1 hour (if available)
            "Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather_info
    else:
        return None

# Home Page (With Live Weather Display)
if page == "Home":
    st.title("🏡 Welcome to AgriShield")
    st.write("🚜 AI-driven Crop Disease Prediction and Farm Monitoring")

    # Load the banner image safely
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"⚠️ Image not found! Please check the file path: `{image_path}`")

    # Display live weather
    st.subheader("🌦 Live Weather Updates")
    
    weather_data = get_weather()
    if weather_data:
        col1, col2, col3 = st.columns(3)
        
        col1.metric(label="🌡 Temperature", value=f"{weather_data['Temperature']}°C")
        col2.metric(label="💧 Humidity", value=f"{weather_data['Humidity']}%")
        col3.metric(label="💨 Wind Speed", value=f"{weather_data['Wind Speed']} m/s")
        
        st.write(f"**🌍 City:** {weather_data['City']}")
        st.write(f"**🌦 Condition:** {weather_data['Condition'].capitalize()}")
        st.write(f"**🌧 Rainfall (last 1 hr):** {weather_data['Rain']} mm")
        st.write(f"🕒 **Last Updated:** {weather_data['Updated']}")
    else:
        st.error("⚠️ Failed to fetch weather data. Please check your API key.")

# NDVI Analysis Page
elif page == "NDVI Analysis":
    show_ndvi_page()

# Placeholder for Leaf Disease Detection
elif page == "Leaf Disease Detection":
    st.title("🍃 Leaf Disease Detection (Coming Soon)")
    st.write("🔬 AI model integration for leaf disease detection is in progress.")

# Placeholder for AI Chatbot
elif page == "Chatbot":
    st.title("💬 AgriShield Chatbot (Coming Soon)")
    st.write("🤖 AI-powered chatbot integration will be added soon.")

# Other Features Placeholder
elif page == "Other Features":
    st.title("📌 Other Features")
    st.write("🔜 More functionalities will be added soon!")
