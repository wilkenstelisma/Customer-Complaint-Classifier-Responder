import streamlit as st
import os
from groq import Groq

# Hardcoded gold_response_to_id from the notebook state
gold_response_to_id = {
    'Company chooses not to provide a public response': 3,
    'Company believes it acted appropriately as authorized by contract or law': 1,
    'Company believes complaint caused principally by actions of third party outside the control or direction of the company': 0,
    "Company can't verify or dispute the facts in the complaint": 2,
    'Company disputes the facts presented in the complaint': 4,
    'Company has responded to the consumer and the CFPB and chooses not to provide a public response': 5
}

# Create a reverse map for efficient lookup of response strings from IDs
id_to_response = {v: k for k, v in gold_response_to_id.items()}

# Dynamically create system_message to ensure the mapping is consistent
system_message = f"""You are an AI assistant that classifies customer complaints based on predefined response categories.\nYou will be provided with examples of customer complaints and their corresponding response IDs.\nYour task is to analyze the new customer complaint and output the ID of the most appropriate response category, **selecting only from the IDs provided in the following mapping of Response to Response_ID:\n{gold_response_to_id}\n\nExamples:\n"""

few_shot_prompt = [{'role':'system', 'content': system_message}]

# --- Prediction Function ---
def predict_response(complaint, client_instance, model_name, few_shot_prompt, id_to_response_map):
    """Predicts the response ID for a given complaint using a few-shot prompt and converts it to the response string."""
    messages = few_shot_prompt + [{'role': 'user', 'content': complaint}]

    try:
        chat_completion = client_instance.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.0 # To make predictions more deterministic for classification
        )
        prediction_id = chat_completion.choices[0].message.content
        try:
            # Attempt to convert prediction_id to int
            prediction_id = int(prediction_id)
            predicted_response = id_to_response_map.get(prediction_id, f"Prediction ID not found in response map: {prediction_id}")
            return predicted_response
        except ValueError:
            return f"Invalid prediction ID received from model: {prediction_id}"
    except Exception as e:
        return f"Error during prediction: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Customer Complaint Classifier")

st.title("Customer Complaint Classifier")

st.markdown("""
This application classifies customer complaints into predefined response categories using an AI model.\n\n### How it Works:\n1. **Input**: You provide a customer complaint in the text box below.\n2. **AI Model**: The app uses a powerful language model (via Groq API) that has been instructed with examples of complaints and their correct classifications.\n3. **Classification**: The model analyzes your complaint and predicts the most appropriate response category from a fixed set of options.\n4. **Output**: The predicted response category is displayed.\n\n""")

st.subheader("API Configuration")
col1, col2 = st.columns([0.7, 0.3])
with col1:
    groq_api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password",
        help="You need a Groq API key to use this application."
    )
with col2:
    st.markdown("""<br>""", unsafe_allow_html=True) # Add a line break for alignment
    st.link_button("Get a Groq API Key", "https://console.groq.com/keys")


if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
        model_name = 'openai/gpt-oss-20b'

        st.subheader("Available Response Categories")
        # Display the mapping for the user
        for response, response_id in gold_response_to_id.items():
            st.write(f"- **ID {response_id}**: {response}")

        st.subheader("Enter a customer complaint:")
        user_complaint = st.text_area("Complaint Text", height=150, placeholder="e.g., I want to sue the bank for abuse")

        if st.button("Classify Complaint"):
            if user_complaint:
                with st.spinner("Classifying complaint..."):
                    predicted_response_text = predict_response(user_complaint, client, model_name, few_shot_prompt, id_to_response)
                    st.success("Classification Complete!")
                    st.write(f"**Predicted Response:** {predicted_response_text}")
            else:
                st.warning("Please enter a complaint to classify.")
    except Exception as e:
        st.error(f"Error initializing Groq client with the provided API key: {e}. Please check your key.")
else:
    st.info("Please enter your Groq API Key to proceed.")

st.markdown("---")
st.markdown("Powered by Groq and Streamlit.")
