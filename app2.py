import streamlit as st
import json
import random
import os

# ✅ Streamlit config must be first
st.set_page_config(page_title="Exam Preparation App", layout="wide")

# ✅ Load and validate question files
@st.cache
def load_all_questions():
    data_folder = "data"
    all_questions = []
    skipped_files = []
    error_files = []

    for file in os.listdir(data_folder):
        if file.endswith(".json"):
            try:
                with open(os.path.join(data_folder, file), 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        all_questions.extend(content)
                    else:
                        skipped_files.append(file)
            except Exception as e:
                error_files.append((file, str(e)))

    return all_questions, skipped_files, error_files

# ✅ Load and handle warning messages
questions, skipped_files, error_files = load_all_questions()
for file in skipped_files:
    st.warning(f"⚠️ Skipped: {file} does not contain a list.")
for file, err in error_files:
    st.warning(f"⚠️ Error reading {file}: {err}")

# ✅ App Title
st.title("🧠 Exam Preparation App")

# ✅ No questions = stop
if not questions:
    st.error("❌ No valid questions found. Please check /data/*.json format.")
    st.stop()

# ✅ Sidebar Preferences
st.sidebar.header("📌 Select Preferences")

categories = sorted(set(q.get('category', 'Uncategorized') for q in questions))
selected_category = st.sidebar.selectbox("Choose a topic:", categories)

# ✅ Only use "MCQ" and "Read"
allowed_types = ["MCQ", "Read"]
question_types = sorted(set(q['type'] for q in questions if q['category'] == selected_category and q['type'] in allowed_types))
selected_type = st.sidebar.radio("Choose question type:", question_types)

# ✅ Filter questions
filtered_qs = [q for q in questions if q['category'] == selected_category and q['type'] == selected_type]
max_q_count = len(filtered_qs)

if max_q_count == 0:
    st.warning("No questions available for the selected type.")
    st.stop()

# ✅ Question count (default 15 or lower max)
default_count = min(15, max_q_count)
num_questions = st.sidebar.slider("How many questions?", 1, max_q_count, default_count)

# ✅ Start
if st.sidebar.button("Start Practice"):
    st.session_state.started = True
    st.session_state.selected_questions = random.sample(filtered_qs, num_questions)
    st.session_state.current_index = 0
    st.session_state.correct_count = 0

# ✅ Show Questions
if st.session_state.get("started", False):
    current_index = st.session_state.current_index
    selected_qs = st.session_state.selected_questions
    current_q = selected_qs[current_index]

    st.subheader(f"Question {current_index + 1} of {len(selected_qs)}")
    st.markdown(f"**{current_q['question']}**")

    user_answer = None
    if current_q['type'] == 'MCQ':
        user_answer = st.radio("Choose an answer:", current_q['options'], key=f"answer_{current_index}")
    elif current_q['type'] == 'Read':
        st.info("🧾 This is a read-only informational question.")
        st.markdown(f"**Answer:** {current_q['answer']}")
        if explanation := current_q.get('explanation'):
            st.info(f"💡 Explanation: {explanation}")

    if current_q['type'] == 'MCQ' and st.button("Submit", key=f"submit_{current_index}"):
        correct = user_answer == current_q['answer']
        if correct:
            st.success("✅ Correct Answer!")
            st.session_state.correct_count += 1
        else:
            st.error(f"❌ Wrong Answer. Correct: {current_q['answer']}")
        if explanation := current_q.get('explanation'):
            st.info(f"💡 Explanation: {explanation}")

        st.session_state.current_index += 1
        st.experimental_rerun()

    if current_q['type'] == 'Read' and st.button("Next", key=f"next_{current_index}"):
        st.session_state.current_index += 1
        st.experimental_rerun()

    # ✅ End of Quiz
    if current_index >= len(selected_qs):
        st.success(f"🎯 Quiz Complete! Your score: {st.session_state.correct_count}/{len(selected_qs)}")
        st.balloons()
        st.session_state.started = False
else:
    st.info("👈 Choose topic and click 'Start Practice' to begin.")
