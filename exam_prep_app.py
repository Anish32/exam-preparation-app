import streamlit as st
import io
import contextlib
import sqlite3
import time

st.set_page_config(page_title="Interview Preparation App", layout="wide")

# --- Sample MCQ Data (global) ---
mcqs = [
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["5", "6", "8", "9"],
        "answer": 2,
        "explanation": "2 ** 3 means 2 raised to the power 3, which is 8.",
        "hint": "** is the exponentiation operator in Python."
    },
    {
        "question": "Which of the following is NOT a Python data structure?",
        "options": ["List", "Dictionary", "Tuple", "Tree"],
        "answer": 3,
        "explanation": "Tree is not a built-in Python data structure.",
        "hint": "Think about built-in types in Python."
    },
    {
        "question": "Which SQL command is used to remove all records from a table, including all spaces allocated for the records?",
        "options": ["DELETE", "REMOVE", "DROP", "TRUNCATE"],
        "answer": 3,
        "explanation": "TRUNCATE removes all rows and frees the space.",
        "hint": "Consider using TRUNCATE for this task."
    },
    {
        "question": "Which library is commonly used for data manipulation in Python?",
        "options": ["NumPy", "Pandas", "Matplotlib", "Seaborn"],
        "answer": 1,
        "explanation": "Pandas is widely used for data manipulation and analysis.",
        "hint": "Pandas is a popular choice for data manipulation in Python."
    },
    {
        "question": "Which of the following is used to handle missing data in pandas?",
        "options": ["fillna()", "dropna()", "isnull()", "All of the above"],
        "answer": 3,
        "explanation": "All these methods are used for handling missing data in pandas.",
        "hint": "Consider using fillna(), dropna(), or isnull() for different scenarios."
    },
    {
        "question": "What does the SQL WHERE clause do?",
        "options": ["Limits the columns returned", "Limits the rows returned", "Sorts the result", "Deletes rows"],
        "answer": 1,
        "explanation": "WHERE limits the rows returned by a query.",
        "hint": "WHERE is used to filter rows in a query."
    },
    {
        "question": "Which of the following is a supervised learning algorithm?",
        "options": ["K-Means Clustering", "Linear Regression", "PCA", "Apriori"],
        "answer": 1,
        "explanation": "Linear Regression is a supervised learning algorithm.",
        "hint": "Linear Regression is a common supervised learning algorithm."
    },
    {
        "question": "What is the output of len(set([1,2,2,3,4,4,4])) in Python?",
        "options": ["4", "5", "6", "7"],
        "answer": 0,
        "explanation": "set() removes duplicates, so the set is {1,2,3,4}, length is 4.",
        "hint": "Use the set() function to remove duplicates."
    },
    {
        "question": "Which SQL keyword is used to sort the result-set?",
        "options": ["ORDER BY", "SORT", "GROUP BY", "ARRANGE"],
        "answer": 0,
        "explanation": "ORDER BY is used to sort the result-set in SQL.",
        "hint": "ORDER BY is used to sort the result-set in SQL."
    },
    {
        "question": "Which function is used to read a CSV file in pandas?",
        "options": ["read_csv()", "readfile()", "load_csv()", "open_csv()"],
        "answer": 0,
        "explanation": "read_csv() is the correct function to read CSV files in pandas.",
        "hint": "Use read_csv() to read CSV files in pandas."
    },
    {
        "question": "Which of the following is NOT a valid Python variable name?",
        "options": ["_var", "var1", "1var", "var_1"],
        "answer": 2,
        "explanation": "Variable names cannot start with a digit.",
        "hint": "Variable names should not start with a digit."
    },
    {
        "question": "Which method can be used to remove whitespace from the beginning and the end of a string in Python?",
        "options": ["strip()", "trim()", "remove()", "clean()"],
        "answer": 0,
        "explanation": "strip() removes whitespace from both ends of a string.",
        "hint": "Use strip() to remove whitespace from both ends of a string."
    },
    {
        "question": "Which SQL statement is used to extract data from a database?",
        "options": ["GET", "OPEN", "SELECT", "EXTRACT"],
        "answer": 2,
        "explanation": "SELECT is used to extract data from a database.",
        "hint": "Use SELECT to extract data from a database."
    },
    {
        "question": "Which of the following is used for data visualization in Python?",
        "options": ["Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
        "answer": 2,
        "explanation": "Matplotlib is a popular data visualization library.",
        "hint": "Matplotlib is a popular data visualization library."
    },
    {
        "question": "Which function returns the number of rows in a pandas DataFrame?",
        "options": ["len(df)", "df.size", "df.shape[0]", "df.count()"],
        "answer": 2,
        "explanation": "df.shape[0] gives the number of rows in a DataFrame.",
        "hint": "Use df.shape[0] to get the number of rows in a DataFrame."
    },
    {
        "question": "Which of the following is used to create a virtual environment in Python?",
        "options": ["venv", "virtualenv", "conda", "All of the above"],
        "answer": 3,
        "explanation": "All these tools can be used to create virtual environments in Python.",
        "hint": "venv, virtualenv, and conda are all valid tools for creating virtual environments in Python."
    },
    {
        "question": "Which SQL clause is used to remove duplicate rows from the result set?",
        "options": ["UNIQUE", "DISTINCT", "REMOVE DUPLICATES", "GROUP BY"],
        "answer": 1,
        "explanation": "DISTINCT removes duplicate rows from the result set.",
        "hint": "Use DISTINCT to remove duplicate rows from the result set."
    },
]

# --- Coding Practice Problems ---
python_problems = [
    {
        "title": "Sum of Two Numbers",
        "description": "Write a function that returns the sum of two numbers.",
        "template": "def sum_two_numbers(a, b):\n    # Write your code here\n    return 0",
        "test_code": "assert sum_two_numbers(2, 3) == 5\nassert sum_two_numbers(-1, 1) == 0",
        "hint": "Use the + operator to add two numbers.",
        "explanation": "The function should return a + b.",
    },
    {
        "title": "Check Palindrome",
        "description": "Write a function to check if a string is a palindrome.",
        "template": "def is_palindrome(s):\n    # Write your code here\n    return False",
        "test_code": "assert is_palindrome('madam') == True\nassert is_palindrome('hello') == False",
        "hint": "A palindrome reads the same forwards and backwards. Try using string slicing.",
        "explanation": "Check if s == s[::-1] to determine if the string is a palindrome.",
    },
    {
        "title": "Find Maximum",
        "description": "Write a function that returns the maximum of three numbers.",
        "template": "def max_of_three(a, b, c):\n    # Write your code here\n    return 0",
        "test_code": "assert max_of_three(1, 2, 3) == 3\nassert max_of_three(10, 5, 7) == 10",
        "hint": "Use the built-in max() function or compare the numbers using if-else.",
        "explanation": "You can use return max(a, b, c) or compare a, b, and c manually.",
    },
    {
        "title": "Fibonacci Number",
        "description": "Write a function that returns the nth Fibonacci number.",
        "template": "def fibonacci(n):\n    # Write your code here\n    return 0",
        "test_code": "assert fibonacci(1) == 1\nassert fibonacci(5) == 5\nassert fibonacci(7) == 13",
        "hint": "The Fibonacci sequence is defined as F(n) = F(n-1) + F(n-2), with F(1)=1, F(2)=1.",
        "explanation": "Use recursion or iteration to compute the nth Fibonacci number.",
    },
]
sql_problems = [
    {
        "title": "Select All",
        "description": "Write a SQL query to select all columns from the employees table.",
        "template": "SELECT ... FROM employees;",
        "solution": "SELECT * FROM employees;",
        "hint": "Use SELECT * FROM employees; to select all columns from the employees table.",
        "explanation": "SELECT * FROM employees; selects all columns from the employees table."
    },
    {
        "title": "Count Rows",
        "description": "Write a SQL query to count the number of employees.",
        "template": "SELECT ... FROM employees;",
        "solution": "SELECT COUNT(*) FROM employees;",
        "hint": "Use COUNT(*) to count the number of rows in a table.",
        "explanation": "SELECT COUNT(*) FROM employees; counts the number of rows in the employees table."
    },
    {
        "title": "Select High Earners",
        "description": "Write a SQL query to select names of employees with salary greater than 75000.",
        "template": "SELECT ... FROM employees WHERE ...;",
        "solution": "SELECT name FROM employees WHERE salary > 75000;",
        "hint": "Use WHERE salary > 75000 to filter employees with a salary greater than 75000.",
        "explanation": "SELECT name FROM employees WHERE salary > 75000; selects names of employees with a salary greater than 75000."
    },
    {
        "title": "Average Salary",
        "description": "Write a SQL query to find the average salary of all employees.",
        "template": "SELECT ... FROM employees;",
        "solution": "SELECT AVG(salary) FROM employees;",
        "hint": "Use AVG(salary) to calculate the average salary of all employees.",
        "explanation": "SELECT AVG(salary) FROM employees; calculates the average salary of all employees in the employees table."
    },
]

# --- Reading Section Data ---
qna_data = {
    "Python": [
        {"q": "What is a list comprehension?", "a": "A concise way to create lists using a single line of code."},
        {"q": "What is the difference between a list and a tuple?", "a": "Lists are mutable, tuples are immutable."},
        {"q": "What is a lambda function?", "a": "An anonymous function expressed as a single statement."},
        {"q": "What is PEP8?", "a": "PEP8 is the Python style guide for writing readable code."},
        {"q": "What is a decorator?", "a": "A function that modifies the behavior of another function."},
    ],
    "SQL": [
        {"q": "What is a JOIN in SQL?", "a": "A JOIN combines rows from two or more tables based on a related column."},
        {"q": "What does GROUP BY do?", "a": "It groups rows that have the same values in specified columns."},
        {"q": "What is a primary key?", "a": "A unique identifier for each record in a table."},
        {"q": "What is a foreign key?", "a": "A key used to link two tables together."},
        {"q": "What is normalization?", "a": "The process of organizing data to reduce redundancy."},
    ],
    "Data Science": [
        {"q": "What is overfitting?", "a": "A model fits the training data too well and fails to generalize to new data."},
        {"q": "What is feature engineering?", "a": "The process of creating new input features from existing ones to improve model performance."},
        {"q": "What is cross-validation?", "a": "A technique for assessing how a model will generalize to an independent dataset."},
        {"q": "What is a confusion matrix?", "a": "A table used to evaluate the performance of a classification model."},
        {"q": "What is regularization?", "a": "A technique to prevent overfitting by adding a penalty to the loss function."},
    ],
}

# --- Coding Practice Performance State ---
if 'python_attempts' not in st.session_state:
    st.session_state.python_attempts = 0
if 'python_success' not in st.session_state:
    st.session_state.python_success = 0
if 'sql_attempts' not in st.session_state:
    st.session_state.sql_attempts = 0
if 'sql_success' not in st.session_state:
    st.session_state.sql_success = 0

# Sidebar navigation
st.sidebar.title("Interview Prep Navigation")
section_options = ["-- Select Section --", "Coding Practice", "Multiple Choice Questions", "Reading Section", "Performance"]
section = st.sidebar.radio("Go to", section_options)

st.title("SmartCrack - Interview Preparation App")
st.subheader("Your smart study companion!")
st.write("Select a topic, choose question type, and start practicing.")

if section == "-- Select Section --":
    st.info("Please select a section from the sidebar to begin.")
elif section == "Coding Practice":
    st.header("[ Coding Practice (Python & SQL) ]")
    tab1, tab2 = st.tabs(["Python", "SQL"])
    with tab1:
        st.subheader("[Python Coding Practice]")
        py_idx = st.selectbox("Select a problem:", list(range(len(python_problems))), format_func=lambda i: python_problems[i]["title"], key="py_problem_select")
        problem = python_problems[py_idx]
        st.write(problem["description"])
        col1, col2 = st.columns([3, 1])
        with col1:
            code = st.text_area("Your code:", value=problem["template"], height=150, key=f"py_code_{py_idx}")
        with col2:
            with st.expander("Hint"):
                st.write(problem.get("hint", "No hint available."))
            with st.expander("Explanation"):
                st.write(problem.get("explanation", "No explanation available."))
        run = st.button("Run Code", key=f"run_py_{py_idx}")
        if run:
            st.session_state.python_attempts += 1
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    exec(code, globals())
                    exec(problem["test_code"], globals())
                st.success("All tests passed!")
                st.session_state.python_success += 1
            except AssertionError:
                st.error("Some tests failed. Check your logic.")
            except Exception as e:
                st.error(f"Error: {e}")
            st.text(output.getvalue())
    with tab2:
        st.subheader("[SQL Coding Practice]")
        sql_idx = st.selectbox("Select a problem:", list(range(len(sql_problems))), format_func=lambda i: sql_problems[i]["title"], key="sql_problem_select")
        problem = sql_problems[sql_idx]
        st.write(problem["description"])
        col1, col2 = st.columns([3, 1])
        with col1:
            user_query = st.text_area("Your SQL query:", value=problem["template"], height=100, key=f"sql_code_{sql_idx}")
        with col2:
            with st.expander("Hint"):
                st.write(problem.get("hint", "Try to use SELECT, WHERE, or aggregate functions as needed."))
            with st.expander("Explanation"):
                st.write(problem.get("explanation", "No explanation available."))
        run_sql = st.button("Run SQL", key=f"run_sql_{sql_idx}")
        if run_sql:
            st.session_state.sql_attempts += 1
            conn = sqlite3.connect(":memory:")
            cur = conn.cursor()
            cur.execute("CREATE TABLE employees (id INTEGER, name TEXT, salary INTEGER);")
            cur.executemany("INSERT INTO employees VALUES (?, ?, ?);", [(1, 'Alice', 70000), (2, 'Bob', 80000), (3, 'Carol', 90000)])
            try:
                cur.execute(user_query)
                rows = cur.fetchall()
                st.success("Query executed!")
                st.dataframe(rows)
                if user_query.strip().lower() == problem["solution"].strip().lower():
                    st.session_state.sql_success += 1
            except Exception as e:
                st.error(f"SQL Error: {e}")
            conn.close()
elif section == "Multiple Choice Questions":
    st.header("[Multiple Choice Questions]")
    if 'mcq_index' not in st.session_state:
        st.session_state.mcq_index = 0
    if 'mcq_score' not in st.session_state:
        st.session_state.mcq_score = 0
    if 'mcq_attempted' not in st.session_state:
        st.session_state.mcq_attempted = 0
    if 'mcq_show_feedback' not in st.session_state:
        st.session_state.mcq_show_feedback = False
    if 'mcq_last_correct' not in st.session_state:
        st.session_state.mcq_last_correct = False
    if 'mcq_last_explanation' not in st.session_state:
        st.session_state.mcq_last_explanation = ''
    if 'mcq_last_answer' not in st.session_state:
        st.session_state.mcq_last_answer = None
    idx = st.session_state.mcq_index
    if idx < len(mcqs):
        q = mcqs[idx]
        st.subheader(f"Question {idx+1} of {len(mcqs)}")
        st.write(q["question"])
        with st.expander("Hint"):
            st.write(q.get("hint", "No hint available."))
        options_with_placeholder = ["-- Select an option --"] + q["options"]
        user_ans = st.radio("Select your answer:", options_with_placeholder, key=f"mcq_{idx}")
        if not st.session_state.mcq_show_feedback:
            if st.button("Submit Answer", key=f"submit_{idx}"):
                if user_ans == "-- Select an option --":
                    st.warning("Please select an option before submitting.")
                else:
                    correct = q["options"].index(user_ans) == q["answer"]
                    st.session_state.mcq_attempted += 1
                    st.session_state.mcq_last_correct = correct
                    st.session_state.mcq_last_explanation = q["explanation"]
                    st.session_state.mcq_last_answer = user_ans
                    st.session_state.mcq_show_feedback = True
                    if correct:
                        st.session_state.mcq_score += 1
                    st.experimental_rerun()
        else:
            if st.session_state.mcq_last_correct:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is: {q['options'][q['answer']]}")
            with st.expander("Explanation"):
                st.write(q.get("explanation", "No explanation available."))
            if st.button("Next Question", key=f"next_{idx}"):
                st.session_state.mcq_index += 1
                st.session_state.mcq_show_feedback = False
                st.session_state.mcq_last_answer = None
                st.experimental_rerun()
    else:
        st.success(f"You have completed all questions!")
        st.write(f"Score: {st.session_state.mcq_score} / {len(mcqs)}")
        st.write(f"Attempted: {st.session_state.mcq_attempted}")
        if st.button("Restart Quiz"):
            st.session_state.mcq_index = 0
            st.session_state.mcq_score = 0
            st.session_state.mcq_attempted = 0
            st.session_state.mcq_show_feedback = False
            st.session_state.mcq_last_answer = None
            st.experimental_rerun()
elif section == "Reading Section":
    st.header("Interview Q&A Reading Section")
    topics = list(qna_data.keys())
    topic = st.selectbox("Select a topic:", topics)
    search = st.text_input("Search questions:")
    filtered = [item for item in qna_data[topic] if search.lower() in item["q"].lower() or search.lower() in item["a"].lower()]
    for item in filtered:
        st.write(f"**Q:** {item['q']}")
        st.write(f"**A:** {item['a']}")
        st.markdown("---")
    if not filtered:
        st.info("No questions found for your search.")
elif section == "Performance":
    st.header("Your Performance")
    st.subheader("MCQ Performance")
    st.write(f"Score: {st.session_state.get('mcq_score', 0)} / {len(mcqs)}")
    st.write(f"Attempted: {st.session_state.get('mcq_attempted', 0)}")
    if st.session_state.get('mcq_attempted', 0) > 0:
        st.progress(st.session_state.get('mcq_score', 0) / max(1, st.session_state.get('mcq_attempted', 0)))
    st.markdown("---")
    st.subheader("Coding Practice Performance")
    st.write(f"Python Problems Attempted: {st.session_state.python_attempts}")
    st.write(f"Python Problems Solved: {st.session_state.python_success}")
    if st.session_state.python_attempts > 0:
        st.progress(st.session_state.python_success / max(1, st.session_state.python_attempts))
    st.write(f"SQL Problems Attempted: {st.session_state.sql_attempts}")
    st.write(f"SQL Problems Solved: {st.session_state.sql_success}")
    if st.session_state.sql_attempts > 0:
        st.progress(st.session_state.sql_success / max(1, st.session_state.sql_attempts)) 