import streamlit as st
import numpy as np
import pickle
import pandas as pd
from PIL import Image

# Load data
df = pd.read_csv('Energy_consumption.csv')

# Load trained model
import joblib

# Load the model
model = joblib.load('energy_model.pkl')


# Streamlit page configuration
st.set_page_config(
    page_title="⚡ Energy Consumption Predictor",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Center the image nicely
image = Image.open('Green tech.jpeg')

# Use columns trick to center the image
col1, col2, col3 = st.columns([1, 2, 1])  # side, center, side
with col1:
    st.write("")  # empty
with col2:
    st.image(image, width=300)  # center image
with col3:
    st.write("")  # empty

# Title and subtitle centered naturally below
st.title("⚡ Energy Consumption Predictor")
st.caption("Predict your building's energy usage based on environmental factors.")

# Section for input fields
st.subheader("🔍 Enter Building and Environmental Conditions")

# Two-column layout for input fields
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("🌡 Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1)
    square_footage = st.number_input("🏢 Square Footage (sq ft)", min_value=100.0, step=10.0)
    occupancy = st.number_input("👥 Number of Occupants", min_value=0, step=1)
    renewable_energy = st.number_input("🌞 Renewable Energy Produced (kWh)", min_value=0.0, step=1.0)
    holiday = st.selectbox("🏖 Is it a Holiday?", ("No", "Yes"))

with col2:
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
    hvac_usage = st.selectbox("🌀 HVAC System On?", ("Yes", "No"))
    lighting_usage = st.selectbox("💡 Lighting System On?", ("Yes", "No"))
    day_of_week = st.selectbox("📅 Day of the Week", 
                               ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))

# Encode categorical inputs
hvac_usage_encoded = 1 if hvac_usage == "Yes" else 0
lighting_usage_encoded = 1 if lighting_usage == "Yes" else 0
holiday_encoded = 1 if holiday == "Yes" else 0
day_of_week_encoded = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}[day_of_week]

# Prepare the input features in the correct order
input_features = np.array([[temperature, humidity, square_footage, occupancy,
                            hvac_usage_encoded, lighting_usage_encoded,
                            renewable_energy, day_of_week_encoded, holiday_encoded]])

# Prediction button
predict_button = st.button("🔮 Predict Energy Consumption")

# Display prediction result
if predict_button:
    prediction = model.predict(input_features)
    st.subheader("Prediction Result")
    st.success(f"🔋 Estimated Energy Consumption: *{prediction[0]:.2f} units*")

