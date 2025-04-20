import streamlit as st
from quiz_agents_image import generate_question, validate_answer, generate_vehicle_image


st.set_page_config(page_title="🚗 Vehicle Brand Quiz", layout="centered")
st.title("🚘 Vehicle Brand Quiz Game")

# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.questions = []
    st.session_state.asked_questions = set()
    st.session_state.show_feedback = False
    st.session_state.last_feedback = ""
    st.session_state.answered = False
    st.session_state.finished = False
    st.session_state.image_url = ""

# Load question if needed
if len(st.session_state.questions) < 5:
    q = generate_question(list(st.session_state.asked_questions))
    st.session_state.questions.append(q)
    st.session_state.asked_questions.add(q["question"])

# Show quiz if not completed
if st.session_state.question_index < 5:
    current_q = st.session_state.questions[st.session_state.question_index]
    st.markdown(f"**Question {st.session_state.question_index + 1}:** {current_q['question']}")

    user_answer = st.radio(
        "Choose your answer:",
        current_q['options'],
        key=f"answer_{st.session_state.question_index}"
    )

    if not st.session_state.answered and st.button("Submit Answer"):
        feedback = validate_answer(current_q['question'], user_answer)
        st.session_state.last_feedback = feedback
        st.session_state.show_feedback = True
        st.session_state.answered = True

        if "result: correct" in feedback.lower():
            st.session_state.score += 1

        # Generate vehicle image for correct brand
        st.session_state.image_url = generate_vehicle_image(current_q['correct_answer'])

    if st.session_state.answered and st.session_state.show_feedback:
        st.markdown("### ✅ Answer Evaluation:")
        st.info(st.session_state.last_feedback)

        if st.session_state.image_url:
            st.image(st.session_state.image_url, caption=f"{current_q['correct_answer']} (AI-generated)", use_column_width=True)

        if st.session_state.question_index < 4:
            if st.button("Next Question"):
                st.session_state.question_index += 1
                st.session_state.show_feedback = False
                st.session_state.last_feedback = ""
                st.session_state.answered = False
                st.rerun()
        elif st.session_state.question_index == 4 and not st.session_state.finished:
            if st.button("Finish Quiz"):
                st.session_state.question_index += 1
                st.session_state.finished = True
                st.rerun()

# Show results after all questions
if st.session_state.question_index >= 5:
    st.markdown("## 🎉 Quiz Completed!")
    st.success(f"**Your Final Score: {st.session_state.score} / 5**")
    if st.button("Play Again"):
        st.session_state.clear()
