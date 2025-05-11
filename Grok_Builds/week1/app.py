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
2. Set your OpenAI API key in a `.env` file (for local use) or Streamlit secrets (for Streamlit Cloud).
3. Run the app: `streamlit run app.py`
"""

# Import standard libraries
import os  # For accessing environment variables and file paths
# Import third-party libraries (but not Streamlit yet)
from dotenv import load_dotenv  # For loading environment variables
# Import local modules
from agent import SimpleAgent  # The AI agent class
from prompts import HEALTHCARE_QUALIFYING_QUESTIONS  # The prompt template

# Debug print to confirm the file version
print("Loading app.py - Version: 2025-05-11 (c1d2e3f4-5a6b-4c7d-8e9f-0a1b2c3d4e5f)")

# Load environment variables from a .env file in the root directory (Grok_AI_Agents)
# Since app.py is in Grok_Builds/week1, we need to go up three levels:
# week1 -> Grok_Builds -> Grok_AI_Agents
# Use os.path.abspath to ensure the path is absolute
script_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to week1
parent_dir = os.path.dirname(script_dir)  # Up to Grok_Builds
root_dir = os.path.dirname(parent_dir)  # Up to Grok_AI_Agents
dotenv_path = os.path.join(root_dir, '.env')

# Load the .env file if it exists (no Streamlit commands used yet)
# Don't fail if the file doesn't exist, as Streamlit Cloud uses Secrets
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"No .env file found at {dotenv_path}. Will attempt to load OPENAI_API_KEY from Streamlit Secrets.")

# Initialize OPENAI_API_KEY as None; we'll set it later
OPENAI_API_KEY = None

# Import Streamlit here to delay its initialization
import streamlit as st

# Debug print before the first Streamlit command
print("First Streamlit command: st.set_page_config()")

# Set the page config as the FIRST Streamlit command at the top level
st.set_page_config(
    page_title="Healthcare Sales Qualifying Questions Generator",
    page_icon="🏥",  # Hospital emoji for the page icon
    layout="centered"  # Center the content for a clean look
)

# Debug print to confirm set_page_config was called
print("st.set_page_config() called successfully")

def run_web_interface():
    """
    Run the Streamlit web interface for the qualifying questions generator.
    
    This function sets up the UI, collects user input, and displays the generated questions.
    It uses the SimpleAgent and prompt template for modularity.
    """
    # Get the OpenAI API key from environment variables (local .env)
    global OPENAI_API_KEY  # Use the global variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # If the API key isn't in the environment variables, try Streamlit secrets (Streamlit Cloud)
    if not OPENAI_API_KEY:
        try:
            print("Attempting to load OPENAI_API_KEY from st.secrets")
            OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
            print("Successfully loaded OPENAI_API_KEY from st.secrets")
        except Exception as e:
            st.error(f"Failed to load OPENAI_API_KEY from environment variables or secrets: {str(e)}")
            st.error("Please set OPENAI_API_KEY in a .env file (locally) or in Streamlit Cloud secrets.")
            st.stop()

    # Final check to ensure we have an API key
    if not OPENAI_API_KEY:
        st.error("OPENAI_API_KEY not found. Please set it in a .env file (locally) or in Streamlit Cloud secrets.")
        st.error("For local use, create a .env file in the root directory (Grok_AI_Agents) with:")
        st.code("OPENAI_API_KEY=your-key-here")
        st.error("For Streamlit Cloud, add OPENAI_API_KEY to the Secrets settings.")
        st.stop()

    # Add a title and description to the UI
    st.title("Healthcare Sales Qualifying Questions Generator")
    st.write("Generate qualifying questions based on a client's situation or pain point.")

    # Create a text area for the user to enter the client situation
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
                    prompt = HEALTHCARE_QUALIFYING_QUESTIONS.format(
                        input=user_goal,
                        num=num_questions
                    )
                    
                    # Use the agent to generate questions
                    questions = agent.generate(prompt)
                    
                    # Check if the correct number of questions was generated
                    if len(questions) != num_questions:
                        st.warning(f"Requested {num_questions} questions, but only {len(questions)} were generated. Try again or adjust the prompt.")
                    
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
    print("Calling run_web_interface() from __main__")
    run_web_interface()