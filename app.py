import streamlit as st
import openai
import os

def generate_itinerary(destination, budget, duration, interests):
    """Generate a travel itinerary using OpenAI API."""
    prompt = f"""
    You are a travel assistant. Generate a {duration}-day itinerary for {destination}.
    The user has a {budget} budget and is interested in {interests}.
    Provide a structured day-by-day plan with activities, accommodations, and food suggestions.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a travel planner."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for security

# Streamlit UI
st.title("AI-Powered Travel Planner")

# User Inputs
destination = st.text_input("Enter your destination:")
budget = st.selectbox("Select your budget:", ["Budget", "Mid-range", "Luxury"])
duration = st.slider("Trip Duration (in days):", 1, 14, 5)
interests = st.text_area("What are your interests? (e.g., history, food, nature)")

if st.button("Generate Itinerary"):
    if destination and interests:
        itinerary = generate_itinerary(destination, budget, duration, interests)
        st.subheader("Your Personalized Itinerary:")
        st.write(itinerary)
    else:
        st.warning("Please enter all required details.")
