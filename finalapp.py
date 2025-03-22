import streamlit as st
import os
import requests
import tensorflow as tf
import numpy as np
from PIL import Image
from datetime import datetime
from ndvi_page import show_ndvi_page  # Import NDVI Analysis Page

# Set page configuration
st.set_page_config(page_title="AgriShield - AI Crop Monitoring", layout="wide")

# Sidebar Navigation (Updated Style)
st.sidebar.title("🌾 AgriShield Navigation")
st.sidebar.markdown("---")  # Separator for cleaner look

# Define pages
PAGES = {
    "Home": "🏡 Home",
    "NDVI Analysis": "🌍 NDVI Analysis",
    "Leaf Disease Detection": "🍃 Leaf Disease Detection",
    "Chatbot": "💬 Chatbot",
    "Other Features": "📌 Other Features"
}

# Custom Navigation using Buttons instead of Radio or Dropdown
selected_page = None
for key, label in PAGES.items():
    if st.sidebar.button(label):
        selected_page = key

if selected_page is None:
    selected_page = "Home"  # Default Page

# OpenWeather API Key
API_KEY = "e15e7551cdb8ed7df8c7fd1833af7fec"
DEFAULT_CITY = "Delhi"
DEFAULT_LAT, DEFAULT_LON = 28.7041, 77.1025  # Default location (Delhi, India)

# Load trained plant disease detection model
model_path = "AgriShield.keras"
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
else:
    model = None

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

# Function to classify leaf disease using the model
def predict_disease(image):
    if model is None:
        return "⚠️ Model not loaded. Please check the file path."

    img = image.resize((128, 128))  # Resize to match model input size
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    
    # Define class labels (Update this with actual labels used in training)
    class_labels = ["Healthy", "Early Blight", "Late Blight", "Bacterial Spot", "Mosaic Virus", "Yellow Leaf Curl Virus"]
    
    return class_labels[class_index] if class_index < len(class_labels) else "Unknown Disease"

# Function for AI Chatbot (Simple Rule-Based)
def chatbot_response(user_input):
    responses = {
        "hello": "Hello! How can I assist you with your crops today?",
        "how are you": "I'm just a bot, but I'm here to help!",
        "weather": "You can check the weather on the Home page.",
        "ndvi": "NDVI Analysis helps in monitoring crop health. Go to the NDVI page for details.",
        "disease": "I can help with plant disease detection! Upload an image in the 'Leaf Disease Detection' section.",
        "bye": "Goodbye! Have a great day on your farm! 🌾"
    }

    user_input = user_input.lower()
    return responses.get(user_input, "I'm not sure, but I'm learning! Try asking about weather, NDVI, or diseases.")

# Home Page (With Live Weather Display)
if selected_page == "Home":
    st.title("🏡 Welcome to AgriShield")
    st.write("🚜 AI-driven Crop Disease Prediction and Farm Monitoring")

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
elif selected_page == "NDVI Analysis":
    show_ndvi_page()

# Leaf Disease Detection Page
elif selected_page == "Leaf Disease Detection":
    st.title("🍃 Leaf Disease Detection")
    st.write("📷 Upload an image of the plant leaf to detect diseases.")

    uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf Image", use_container_width=True)
        
        if st.button("🔍 Analyze"):
            result = predict_disease(image)
            st.success(f"🩺 **Prediction:** {result}")

# AI Chatbot Page
elif selected_page == "Chatbot":
    st.title("💬 AgriShield Chatbot")
    st.write("🤖 Ask any farming-related questions below!")

    user_input = st.text_input("Type your message here...")
    if user_input:
        bot_response = chatbot_response(user_input)
        st.write(f"**🤖 Chatbot:** {bot_response}")

# Other Features Placeholder
elif selected_page == "Other Features":
    st.title("📌 Other Features")
    st.write("🔜 More functionalities will be added soon!")
