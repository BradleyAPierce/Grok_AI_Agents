"""
agent.py
========
Defines a SimpleAgent class for interacting with OpenAI's API.

This class provides a generic way to send prompts to an LLM and parse JSON responses.
It's designed to be reusable for any task by accepting a prompt and model configuration.

Author: Bradley Pierce
Date Created: May 10, 2025
"""

# Import required libraries
import openai  # For interacting with OpenAI's API
import json  # For parsing JSON responses from the LLM

class SimpleAgent:
    """
    A generic AI agent for interacting with OpenAI's language models.
    
    This class handles API authentication, prompt submission, and response parsing.
    It's designed to be simple and reusable for various tasks.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the agent with an API key and model.
        
        Args:
            api_key (str): OpenAI API key for authentication.
            model (str): The LLM model to use (default: gpt-3.5-turbo).
        """
        # Set the API key for OpenAI's client
        # This authenticates all API requests
        openai.api_key = api_key
        # Store the model name (e.g., gpt-3.5-turbo)
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.0) -> list:
        """
        Send a prompt to the LLM and return the parsed JSON response.
        
        Args:
            prompt (str): The prompt to send to the LLM.
            temperature (float): Controls randomness (0.0 = deterministic, default).
        
        Returns:
            list: A list of dictionaries parsed from the JSON response.
        
        This method assumes the LLM returns JSON (e.g., [{"question": "...", "explanation": "..."}]).
        """
        try:
            # Send the prompt to OpenAI's ChatCompletion endpoint
            # The messages list defines the conversation (here, just one user message)
            response = openai.ChatCompletion.create(
                model=self.model,  # Use the specified model
                messages=[  # Send the prompt as a user message
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature  # Control output randomness
            )
            
            # Extract the response text from the first choice
            # The response is a string containing JSON
            response_text = response.choices[0].message.content
            
            # Parse the JSON string into a Python list of dictionaries
            result = json.loads(response_text)
            
            # Return the parsed result
            return result
        
        except Exception as e:
            # If an error occurs (e.g., API failure, invalid JSON), raise an exception
            raise Exception(f"Error generating response: {str(e)}")