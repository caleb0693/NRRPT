import streamlit as st
import pandas as pd
import numpy as np

# Load CSV file
@st.cache
def load_data():
    return pd.read_csv('questions3.csv')

data = load_data()

st.title("NRRPT Practice Exam App")
st.markdown(" #### Created by Caleb Ginorio")
st.markdown("Select the desired number of practice questions from the sidebar")
st.markdown ("Questions obtained from the NRRPT website")
st.markdown("https://www.nrrpt.org")

num_questions = st.sidebar.slider("Number of questions", 5, 25, 25)

if "start_exam" not in st.session_state:
    st.session_state.start_exam = False
    st.session_state.user_answers = [None] * num_questions
    st.session_state.questions_df = data.sample(n=num_questions).reset_index(drop=True)

start_exam = st.button("Start New Exam")
if start_exam:
    st.session_state.start_exam = True
    st.session_state.user_answers = [None] * num_questions
    st.session_state.questions_df = data.sample(n=num_questions).reset_index(drop=True)

if st.session_state.start_exam:
    for i in range(num_questions):
        question = st.session_state.questions_df.iloc[i]
        options = [question[f"option {j}"] for j in range(1, 6)]
        st.session_state.user_answers[i] = st.radio(f"Q{i+1}: {question['question']}", options, key=f"question_{i}")

    submit = st.button("Submit")
    if submit:
        correct_answers = 0
        for i, user_answer in enumerate(st.session_state.user_answers):
            correct_option = st.session_state.questions_df.iloc[i]['answer']
            correct_answer = st.session_state.questions_df.iloc[i][f"option {correct_option + 1}"]
            explanation = st.session_state.questions_df.iloc[i]['explanation']
            if user_answer == correct_answer:
                correct_answers += 1
                color = "green"
            else:
                color = "red"

            st.markdown(f'<p style="color: {color};">Q{i+1}: {st.session_state.questions_df.iloc[i]["question"]}</p>', unsafe_allow_html=True)
            st.write(f"Your answer: {user_answer}")
            st.write(f"Correct answer: {correct_answer}")
            if not pd.isna(explanation):
                st.write(f"Explanation: {explanation}")
            st.write('-' * 40)

        st.write(f"Your score: {correct_answers}/{num_questions} ({(correct_answers / num_questions) * 100:.2f}%)")
