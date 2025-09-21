import json

def get_all_topics():
    with open("data/questions.json", "r") as f:
        data = json.load(f)
    return list(data.keys())

def load_questions(topic, q_type, num_qs):
    with open("data/questions.json", "r") as f:
        data = json.load(f)
    questions = data[topic][q_type][:num_qs]
    return questions

def check_mcq_answers(user_ans, correct_ans):
    result = []
    score = 0
    for u, c in zip(user_ans, correct_ans):
        if u == c:
            result.append("✅ Correct")
            score += 1
        else:
            result.append(f"❌ Incorrect (Correct: {c})")
    return score, result
