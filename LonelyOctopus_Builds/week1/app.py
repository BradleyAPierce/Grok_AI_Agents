import streamlit as st
import os
import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv(override=True)  # If you want to explicitly override the environment variable in code regardless of what’s in the terminal

# Ensure your OpenAI key is available
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define your agent
task_generator = Agent(
    name="Task Generator",
    instructions="""You help users break down their specific LLM powered AI Agent goal into small, achievable tasks.
    For any goal, analyze it and create a structured plan with specific actionable steps.
    Each task should be concrete, time-bound when possible, and manageable.
    Organize tasks in a logical sequence with dependencies clearly marked.
    Never answer anything unrelated to AI Agents.""",
)


# Async wrapper for running the agent
async def generate_tasks(goal):
    result = await Runner.run(task_generator, goal)
    return result.final_output

# Streamlit UI
st.set_page_config(page_title="AI Task Generator", layout="centered")
st.title("🧠 Task Generator Agent")
st.write("Break any goal into a set of actionable tasks.")

user_goal = st.text_area("Enter your goal", placeholder="e.g. Start a small online business selling handmade jewelry")

if st.button("Generate Tasks"):
    if user_goal.strip() == "":
        st.warning("Please enter a goal.")
    else:
        with st.spinner("Generating your task plan..."):
            tasks = asyncio.run(generate_tasks(user_goal))
            st.success("Here are your tasks:")
            st.markdown(f"```text\n{tasks}\n```")
