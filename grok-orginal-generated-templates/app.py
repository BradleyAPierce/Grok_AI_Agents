"""
app.py
======
A Streamlit web interface for the Healthcare Sales Qualifying Questions Generator.

This app uses the SimpleAgent class and prompt templates to generate qualifying questions
based on a user-provided client situation. It's designed to be beginner-friendly and reusable.

Author: Bradley Pierce
Date Created: May 10, 2025

How to Run:
-----------
1. Install requirements: `pip install openai streamlit python-dotenv`
2. Set your OpenAI API key in a `.env` file or Streamlit secrets.
3. Run the app: `streamlit run app.py`
"""

# Import standard libraries
import os  # For accessing environment variables
# Import third-party libraries
import streamlit as st  # For building the web interface
from dotenv import load_dotenv  # For loading environment variables
# Import local modules
from agent import SimpleAgent  # The AI agent class
from prompts import HEALTHCARE_QUALIFYING_QUESTIONS  # The prompt template

# Load environment variables from a .env file (if it exists)
# This allows secure storage of the API key
load_dotenv()

# Get the OpenAI API key from environment variables or Streamlit secrets
# Streamlit secrets are used for deployment on Streamlit Cloud
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# Check if the API key is available; if not, show an error and stop the app
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in a .env file or Streamlit secrets.")
    st.stop()

def run_web_interface():
    """
    Run the Streamlit web interface for the qualifying questions generator.
    
    This function sets up the UI, collects user input, and displays the generated questions.
    It uses the SimpleAgent and prompt template for modularity.
    """
    # Configure the Streamlit page (title, icon, layout)
    st.set_page_config(
        page_title="Healthcare Sales Qualifying Questions Generator",
        page_icon="🏥",  # Hospital emoji for the page icon
        layout="centered"  # Center the content for a clean look
    )
    
    # Add a title and description to the UI
    st.title("Healthcare Sales Qualifying Questions Generator")
    st.write("Generate qualifying questions based on a client's situation or pain point.")
    
    # Create a text area for the user to enter the client situation
    # The placeholder provides an example to guide the user
    user_goal = st.text_area(
        "Enter the client's situation or pain point",
        placeholder="e.g., Client is struggling with patient data management and compliance"
    )
    
    # Add a number input for the user to specify the number of questions
    num_questions = st.number_input(
        "Number of questions to generate",
        min_value=1,
        max_value=20,
        value=10  # Default to 10 questions
    )
    
    # Add a button to trigger question generation
    if st.button("Generate Questions"):
        # Check if the user provided input; if not, show a warning
        if not user_goal.strip():
            st.warning("Please enter a client situation or pain point.")
        else:
            # Show a spinner while generating questions to indicate progress
            with st.spinner("Generating your qualifying questions..."):
                try:
                    # Create an instance of the SimpleAgent with the API key
                    agent = SimpleAgent(api_key=OPENAI_API_KEY)
                    
                    # Format the prompt with the user’s input and number of questions
                    # This replaces {input} and {num} in the prompt template
                    prompt = HEALTHCARE_QUALIFYING_QUESTIONS.format(
                        input=user_goal,
                        num=num_questions
                    )
                    
                    # Use the agent to generate questions
                    # The agent returns a list of dictionaries (parsed JSON)
                    questions = agent.generate(prompt)
                    
                    # Check if questions were generated successfully
                    if questions:
                        # Display a success message with the number of questions
                        st.success(f"Here are your {len(questions)} qualifying questions:")
                        
                        # Loop through the questions and display each one
                        for i, item in enumerate(questions, 1):
                            # Use markdown for formatted text (bold question, italic explanation)
                            st.markdown(f"**Question {i}:** {item['question']}")
                            st.markdown(f"*Explanation:* {item['explanation']}")
                            st.markdown("---")  # Add a separator between questions
                    else:
                        # If no questions were generated, show an error
                        st.error("No questions were generated. Please try again.")
                
                except Exception as e:
                    # If an error occurs (e.g., API failure), show an error
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    """
    Entry point of the script.
    
    This block runs when the script is executed directly (e.g., `python app.py`).
    It starts the Streamlit web interface.
    """
    run_web_interface()