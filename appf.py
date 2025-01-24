import streamlit as st
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import csv
from datetime import datetime
import os

# Initialize Model
model = SentenceTransformer('all-MiniLM-L6-v2')
classifier = pipeline('sentiment-analysis')

# CSV File to store user data and reports
CSV_FILE = 'user_reports.csv'

# Function to analyze mental state
def detect_disorder(user_input):
    embeddings = model.encode(user_input, convert_to_tensor=True)
    sentiment = classifier(user_input)[0]
    return sentiment['label'], sentiment['score']

# Function to generate a comprehensive suggestion
def generate_suggestion(feeling_desc, symptom):
    base_advice = (
        f"It sounds like you're experiencing feelings of '{feeling_desc}'. This could indicate that you may be "
        f"dealing with '{symptom.lower()}' symptoms. Here are some steps that might help you manage these feelings:\n\n"
    )
    
    if symptom == "NEGATIVE":
        additional_advice = (
            "- **Acknowledge Your Feelings**: It's okay to feel this way. Sometimes, allowing yourself to accept and express your emotions can bring relief.\n"
            "- **Practice Self-Care**: Engage in activities you enjoy, such as reading, meditating, or spending time with loved ones.\n"
            "- **Physical Activity**: Exercise can help elevate mood by releasing endorphins. Try going for a walk, yoga, or any activity that gets you moving.\n"
            "- **Reach Out to Friends/Family**: Connecting with others can provide emotional support and help you feel understood.\n"
            "- **Consider Professional Help**: Talking to a professional can provide structured support and guidance.\n\n"
        )
    else:
        additional_advice = (
            "- **Maintain Positivity**: Keep nurturing these positive feelings by focusing on what brings you joy and purpose.\n"
            "- **Set Small Goals**: Achieving small goals can enhance your mood and give a sense of accomplishment.\n"
            "- **Stay Connected**: Share your positive experiences with friends and family to strengthen your bonds.\n"
            "- **Reflect on Gratitude**: Taking a moment to appreciate the good things can reinforce positive emotions.\n\n"
        )
    
    professional_help = (
        "\n---\n\n**Need More Help?**\n\n"
        "If you're experiencing persistent symptoms or distress, consider reaching out to a licensed psychologist. "
        "Professional support can provide you with personalized care and guidance. [Find a psychologist here](https://www.example-psychologist-link.com).\n\n"
    )

    detailed_report = base_advice + additional_advice + professional_help
    return detailed_report

# Function to store user details and report in CSV
def save_to_csv(name, gender, dob, user_input, detected_symptom, confidence, suggestion):
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([report_time, name, gender, dob, user_input, detected_symptom, confidence, suggestion])

# Load user reports from CSV
def load_reports():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=['Time', 'Name', 'Gender', 'DOB', 'User Input', 'Detected Symptom', 'Confidence', 'Suggestion'])
    return pd.read_csv(CSV_FILE)

# Streamlit App Interface
st.title("Cognitive Disorder Detection Chatbot")

# Main Menu
menu = st.sidebar.selectbox("Menu", ["Home", "View Reports"])

if menu == "Home":
    st.header("User Information")
    name = st.text_input("Enter your name:")
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
    dob = st.date_input("Enter your date of birth:")

    if st.button("Proceed"):
        st.session_state.user_info = (name, gender, dob)

    # Emotion Description Section
    if "user_info" in st.session_state:
        st.header("Describe your current emotional state:")
        user_input = st.text_area("How are you feeling today?")
        
        if st.button("Analyze"):
            detected_symptom, confidence = detect_disorder(user_input)
            suggestion = generate_suggestion(user_input, detected_symptom)
            
            # Display the full report
            st.subheader("Detailed Report")
            st.write(f"**Name**: {st.session_state.user_info[0]}")
            st.write(f"**Gender**: {st.session_state.user_info[1]}")
            st.write(f"**Date of Birth**: {st.session_state.user_info[2]}")
            st.write(f"**User Input**: {user_input}")
            st.write(f"**Detected Symptom**: {detected_symptom}")
            st.write(f"**Confidence Score**: {confidence:.2f}")
            st.write("**Personalized Suggestion**:")
            st.write(suggestion)

            # Save report to CSV
            save_to_csv(name, gender, dob, user_input, detected_symptom, confidence, suggestion)

elif menu == "View Reports":
    st.header("User Reports")
    reports_df = load_reports()
    st.write(reports_df)
