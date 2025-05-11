"""
cli.py
======
A command-line interface (CLI) for the Healthcare Sales Qualifying Questions Generator.

This script lets you generate questions by running the script from the terminal,
using the same agent and prompts as the Streamlit app.

Author: Bradley Pierce
Date Created: May 10, 2025

How to Run:
-----------
1. Ensure you're in the GROK_AI_AGENT/Grok_Builds/week1 directory.
2. Run: python cli.py "Your client situation here"
   Example: python cli.py "Client is struggling with patient data"
"""
# Import standard libraries
import sys  # For accessing command-line arguments
import os  # For accessing environment variables
# Import local modules
from agent import SimpleAgent  # The AI agent class
from prompts import HEALTHCARE_QUALIFYING_QUESTIONS  # The prompt template
from dotenv import load_dotenv  # For loading the .env file

# Load the .env file from the root directory
# We need to specify the path since cli.py is in a subdirectory (week1)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Get the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

def run_cli():
    """
    Run the CLI to generate qualifying questions based on a client situation.
    
    This function takes the client situation as a command-line argument,
    generates questions, and prints them to the terminal.
    """
    # Check if a client situation was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python cli.py \"Your client situation here\"")
        print("Example: python cli.py \"Client is struggling with patient data\"")
        sys.exit(1)
    
    # Get the client situation from the command-line argument
    user_goal = sys.argv[1]
    
    # Set the number of questions (hardcoded for simplicity, but you can modify this)
    num_questions = 5
    
    try:
        # Create an instance of the SimpleAgent with the API key
        agent = SimpleAgent(api_key=OPENAI_API_KEY)
        
        # Format the prompt with the user’s input and number of questions
        prompt = HEALTHCARE_QUALIFYING_QUESTIONS.format(
            input=user_goal,
            num=num_questions
        )
        
        # Generate the questions using the agent
        questions = agent.generate(prompt)
        
        # Print the generated questions
        print(f"\nGenerated {len(questions)} Qualifying Questions for: {user_goal}\n")
        for i, item in enumerate(questions, 1):
            print(f"Question {i}: {item['question']}")
            print(f"Explanation: {item['explanation']}")
            print("-" * 80)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point of the script.
    
    This block runs when the script is executed directly (e.g., `python cli.py`).
    """
    run_cli()