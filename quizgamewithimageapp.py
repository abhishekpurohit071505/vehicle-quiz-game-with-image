import streamlit as st
from quiz_agents_image import generate_question, generate_explanation, generate_vehicle_image

st.set_page_config(page_title="Vehicle Quiz Game", layout="centered")
st.title("🚗 Vehicle Quiz Game")

# Initialize session state
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()
if "score" not in st.session_state:
    st.session_state.score = 0

# Generate new question
if st.button("🔄 New Question") or "current_question" not in st.session_state:
    q = generate_question(list(st.session_state.asked_questions))
    st.session_state.current_question = q
    st.session_state.selected_answer = None
    st.session_state.correct_answer = q["answer"]
    st.session_state.asked_questions.add(q["question"])
    st.session_state.explanation = ""
    st.session_state.image_url = ""

# Display question
q = st.session_state.current_question
st.markdown(f"### ❓ {q['question']}")
for i, option in enumerate(q["options"]):
    if st.radio("Choose your answer:", q["options"], index=-1, key=q["question"]):
        st.session_state.selected_answer = st.session_state[q["question"]]

# Submit answer
if st.button("✅ Submit Answer") and st.session_state.selected_answer:
    correct = st.session_state.selected_answer == st.session_state.correct_answer
    if correct:
        st.success("Correct! 🎉")
        st.session_state.score += 1
    else:
        st.error(f"Wrong! The correct answer was: {st.session_state.correct_answer}")

    # Generate explanation
    #st.session_state.explanation = generate_explanation(st.session_state.correct_answer)
    #st.markdown(f"**💡 Why?** {st.session_state.explanation}")

    # Generate image for correct brand
    st.session_state.image_url = generate_vehicle_image(st.session_state.correct_answer)
    st.image(st.session_state.image_url, caption=f"{st.session_state.correct_answer} (AI-generated)", use_column_width=True)

# Show score
st.markdown(f"### 🏆 Score: {st.session_state.score}")
