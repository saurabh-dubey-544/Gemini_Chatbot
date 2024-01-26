import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai



load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model
model = genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def generate_gemini_pro_response(user_input):
    response = chat.send_message(user_input)
    return response.text




# Initialize the list of questions and answers
questions = []
answers = []

# Create a function to add a new question and answer to the list
def add_question_answer(question, answer):
    questions.append(question)
    answers.append(answer)

# Create a function to display the questions and answers
def display_questions_answers():
    for i in range(len(questions)):
        st.write(f"Question: {questions[i]}")
        st.write(f"Answer: {answers[i]}")

# Create a sidebar for user input
st.sidebar.title("Ask a Question")
question = st.sidebar.text_input("Question")
answer = generate_gemini_pro_response(question)

# Create a button for the user to submit their question
if st.sidebar.button("Submit"):
    # Add the question and answer to the list
    add_question_answer(question, answer)
    # Display the questions and answers
    display_questions_answers()