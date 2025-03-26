import streamlit as st
import datetime
import requests
import os
from dotenv import load_dotenv

# --- Load API Key from .env ---
load_dotenv()  # Load environment variables from .env
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Get API key securely
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# --- Helper Function to Get Response from Together AI ---
def get_together_response(prompt):
    """Fetches a response from Together AI based on the user prompt."""
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",  # Choose appropriate model
        "messages": [
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    
    response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Streamlit UI ---
st.title("🌍 AI-Powered Trip Planner (Together AI Edition)")
st.write("Plan your perfect trip with personalized recommendations powered by Together AI!")

# Collecting User Inputs with Forms
with st.form("trip_form"):
    destination = st.text_input("📍 Where are you traveling to?")
    start_date = st.date_input("📅 Start Date", datetime.date.today())
    end_date = st.date_input("📅 End Date", datetime.date.today())
    budget = st.selectbox("💸 What is your budget?", ["Budget", "Moderate", "Luxury"])
    interests = st.text_input("🎯 What activities or interests do you have?")
    dietary = st.text_input("🍽 Any dietary preferences?")
    mobility = st.selectbox("🦽 Do you have any mobility concerns?", ["None", "Limited", "Wheelchair Accessible"])
    accommodation = st.selectbox("🏨 Accommodation preference", ["Budget", "Moderate", "Luxury", "Central Location"])
    submit_button = st.form_submit_button("✨ Get My Itinerary")

# --- Validate and Process User Input ---
if submit_button:
    if destination and start_date and end_date:
        days = (end_date - start_date).days + 1

        # --- Build User Context Prompt ---
        user_input_prompt = f"Generate a {days}-day itinerary for a trip to {destination} with a {budget.lower()} budget. "
        user_input_prompt += f"Interests include {interests}. "
        
        if dietary:
            user_input_prompt += f"Consider dietary preferences: {dietary}. "
        if mobility != "None":
            user_input_prompt += f"Ensure activities are {mobility.lower()} friendly. "
        user_input_prompt += f"Stay in a {accommodation.lower()} accommodation."

        # --- Get Response from Together AI ---
        itinerary = get_together_response(user_input_prompt)
        
        # --- Display Itinerary ---
        st.subheader("📅 Your Personalized Itinerary")
        st.write(itinerary)
    else:
        st.warning("⚠ Please fill in all required fields!")