import streamlit as st
import json
import random
import os

# Load questions from the selected category
def load_questions(category):
    with open("data/exam_questions.json", "r") as f:
        all_data = json.load(f)
    return all_data.get(category, [])

# App UI
st.title("📚 Exam Prep App")

with open("data/exam_questions.json", "r") as f:
    all_categories = list(json.load(f).keys())

selected_category = st.selectbox("Select Category:", all_categories)

if selected_category:
    questions = load_questions(selected_category)
    total_questions = st.number_input("How many questions?", min_value=1, max_value=len(questions), value=min(5, len(questions)), step=1)

    if "quiz_started" not in st.session_state or st.button("Start Over"):
        st.session_state.quiz_started = True
        st.session_state.selected_questions = random.sample(questions, total_questions)
        st.session_state.current_q_index = 0
        st.session_state.correct_count = 0

    if st.session_state.quiz_started:
        current_q_index = st.session_state.current_q_index
        current_q = st.session_state.selected_questions[current_q_index]

        st.write(f"### Question {current_q_index + 1} of {total_questions}")
        st.write(current_q['question'])

        if current_q['type'] == 'MCQ':
            options = ["-- Select an answer --"] + current_q['options']
            user_answer = st.radio("Select your answer:", options, key=f"q_{current_q_index}")
        else:
            user_answer = st.text_input("Write your answer:", key=f"q_{current_q_index}")

        if st.button("Submit", key=f"submit_{current_q_index}"):
            if current_q['type'] == 'MCQ' and user_answer == "-- Select an answer --":
                st.warning("Please select an answer.")
                st.stop()

            correct = False
            if current_q['type'] == 'MCQ':
                correct = (user_answer == current_q['answer'])
            else:
                correct = (user_answer.strip().lower() == current_q['answer'].strip().lower())

            if correct:
                st.success("✅ Correct Answer!")
                st.session_state.correct_count += 1
            else:
                st.error(f"❌ Wrong Answer. Correct: {current_q['answer']}")
            st.info(f"💡 Explanation: {current_q.get('explanation', 'No explanation provided.')}")

            if current_q_index + 1 < total_questions:
                if st.button("Next"):
                    st.session_state.current_q_index += 1
            else:
                st.success(f"🎉 Quiz Complete! Your Score: {st.session_state.correct_count}/{total_questions}")
                if st.button("Start Again"):
                    del st.session_state.quiz_started
                    st.rerun()
