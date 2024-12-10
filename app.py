import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debugging: Check if the key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("API key not loaded. Check your .env file and ensure it is in the correct location.")
else:
    print("API key loaded successfully.")


# Streamlit app title and description
st.title("Custom Email Draft Generator")
st.subheader("Generate professional email drafts effortlessly!")

# User inputs
with st.form("email_form"):
    recipient = st.text_input("Who is the email for? (e.g., Hiring Manager, Team, etc.)")
    purpose = st.text_area("What is the purpose of the email?")
    tone = st.selectbox("Select the tone of the email:", ["Formal", "Casual", "Friendly"])
    additional_details = st.text_area("Any additional details you'd like to include (optional):")
    submitted = st.form_submit_button("Generate Email")

# Generate the email
if submitted:
    if not recipient or not purpose:
        st.error("Please fill out all required fields (Recipient and Purpose).")
    else:
        with st.spinner("Generating your email..."):
            try:
                # Construct the message for the ChatCompletion API
                messages = [
                    {"role": "system", "content": "You are an email writing assistant."},
                    {
                        "role": "user",
                        "content": f"""
                        Write an email to {recipient} with the following details:
                        Purpose: {purpose}
                        Tone: {tone}
                        Additional Details: {additional_details if additional_details else 'None'}
                        """,
                    },
                ]

                # Call the ChatCompletion API (new method)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # You can also use "gpt-4" here
                    messages=messages,
                    max_tokens=250,
                    temperature=0.7,
                )

                # Extract the generated email
                email_draft = response["choices"][0]["message"]["content"].strip()

                # Display the result
                st.success("Here is your email draft:")
                st.text_area("Generated Email", email_draft, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")
