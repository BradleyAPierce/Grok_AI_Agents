"""
prompts.py
==========
Defines reusable prompt templates for AI agent tasks.

This file stores prompts as string templates with placeholders (e.g., {input}, {num})
that can be formatted with task-specific data. Each prompt is designed to produce
JSON output for reliable parsing.

Author: Bradley Pierce
Date Created: May 10, 2025
"""

# Define a prompt template for generating healthcare sales qualifying questions
# The template uses placeholders for the client situation and number of questions
# It instructs the LLM to return JSON with question content (labels will be added by the code)
HEALTHCARE_QUALIFYING_QUESTIONS = """
You are a healthcare sales expert. Based on this client situation: {input}

Generate exactly {num} qualifying questions to understand the client's needs and pain points.
For each question, provide an explanation of why it's effective.

Return the response in JSON format, like this:
[
    {{"question": "What specific challenges are you facing?", "explanation": "This helps identify core issues."}},
    {{"question": "How are you currently addressing this?", "explanation": "This reveals their current approach."}},
    ...
]
"""

# You can add more prompt templates here for other tasks
# Example placeholder for a future task (e.g., customer support questions)
CUSTOMER_SUPPORT_QUESTIONS = """
You are a customer support specialist. Based on this issue: {input}

Generate exactly {num} questions to diagnose the customer's problem.

Return the response in JSON format, like this:
[
    {{"question": "Can you describe the issue in detail?", "explanation": "This helps gather more context."}},
    ...
]
"""