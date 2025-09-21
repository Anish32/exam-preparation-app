# app.py
import streamlit as st
import json
import random
import os

# Load questions from JSON file
def load_questions(path):
    with open(path, 'r') as file:
        return json.load(file)

# App layout
st.set_page_config(page_title="Exam Practice App", layout="wide")
st.title("🧠 Exam Preparation App")

# Load question data
DATA_PATH = "exam_questions_sample.json"
if not os.path.exists(DATA_PATH):
    st.error("❌ No questions file found. Please make sure 'exam_questions_sample.json' exists.")
    st.stop()

questions = load_questions(DATA_PATH)

# Sidebar for topic and question type selection
st.sidebar.header("📌 Select Preferences")
categories = sorted(set(q['category'] for q in questions))
selected_category = st.sidebar.selectbox("Choose a topic:", categories)

question_types = sorted(set(q['type'] for q in questions if q['category'] == selected_category))
selected_type = st.sidebar.radio("Choose question type:", question_types)

# Number of questions to attempt
max_q_count = len([q for q in questions if q['category'] == selected_category and q['type'] == selected_type])
if max_q_count == 1:
    num_questions = 1
    st.sidebar.markdown("✅ Only 1 question available for this selection.")
else:
    num_questions = st.sidebar.slider("How many questions?", 1, max_q_count, min(5, max_q_count))


# Start button
if st.sidebar.button("Start Practice"):
    st.session_state.started = True
    st.session_state.selected_questions = random.sample(
        [q for q in questions if q['category'] == selected_category and q['type'] == selected_type],
        num_questions
    )
    st.session_state.current_index = 0
    st.session_state.correct_count = 0

if 'started' in st.session_state and st.session_state.started:
    current_q_index = st.session_state.current_index
    selected_questions = st.session_state.selected_questions
    current_q = selected_questions[current_q_index]

    st.subheader(f"Question {current_q_index + 1} of {len(selected_questions)}")
    st.markdown(f"**{current_q['question']}**")

    user_answer = None

    if current_q['type'] == 'MCQ':
        options_with_placeholder = ["-- Select an answer --"] + current_q['options']
        user_answer = st.radio("Select your answer:", options_with_placeholder, key=f"q_{current_q_index}")

    elif current_q['type'] == 'Written':
        user_answer = st.text_area("Write your answer:")

    if st.button("Submit"):
        correct = False
        if current_q['type'] == 'MCQ':
            correct = (user_answer == current_q['answer'])
        elif current_q['type'] == 'Written':
            correct = (user_answer.strip().lower() == current_q['answer'].strip().lower())

        if correct:
            st.success("✅ Correct Answer!")
            st.session_state.correct_count += 1
        else:
            st.error(f"❌ Wrong Answer. Correct: {current_q['answer']}")
        st.info(f"💡 Explanation: {current_q.get('explanation', 'No explanation available.')}")

        if current_q_index + 1 < len(selected_questions):
            if st.button("Next Question"):
                st.session_state.current_index += 1
                st.experimental_rerun()
        else:
            st.success(f"🎯 You've completed the quiz! Score: {st.session_state.correct_count}/{len(selected_questions)}")
            st.balloons()
            st.session_state.started = False
else:
    st.info("👈 Choose your topic and click 'Start Practice' to begin.")
