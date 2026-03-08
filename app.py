import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Stop if API key is missing
if not api_key:
    st.error("OPENAI_API_KEY not found. Please set it in your .env file.")
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Load context file
try:
    with open("grafton.txt", "r", encoding="utf-8") as file:
        context_text = file.read()
except FileNotFoundError:
    st.error("grafton.txt not found in this folder.")
    st.stop()

# App UI
st.title("Ask Grafton Chatbot")

user_input = st.text_input("Ask a question about Grafton history:")

if st.button("Get Answer"):
    if user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a careful historical assistant. "
                            "Answer ONLY using the provided CONTEXT. "
                            "If the answer is not in the context, say: "
                            "'I don't know based on the provided materials.'"
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"CONTEXT:\n{context_text}\n\nQUESTION:\n{user_input}",
                    },
                ],
                temperature=0.2,
            )

            answer = response.choices[0].message.content
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.write("Please ask a question.")