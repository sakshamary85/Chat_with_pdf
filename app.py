import streamlit as st
import os
from backend.file_handler import extract_text
from backend.summarizer import generate_summary
from backend.question_answer_engine import prepare_retriever, answer_question
from backend.challenge import generate_challenge_questions,evaluate_answers


# ---- Disable LangChain telemetry warnings ----
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
os.environ["LANGCHAIN_API_KEY"] = ""

# ---- Session State Initialization ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "raw_text" not in st.session_state:
    st.session_state.raw_text = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None


# ---- Chat Display Function ----
def show_chat():
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)


# ---- App Title ----
st.set_page_config(page_title="AI PDF Assistant", layout="centered")
st.title("📘 AI PDF Assistant")

# ---- File Upload ----
MAX_FILE_SIZE_MB = 50
st.markdown("#### Upload a document")
st.markdown("**Max file size: 50 MB | Accepted: PDF, TXT**")
uploaded_file = st.file_uploader(" ",type=["pdf", "txt"])
if uploaded_file is not None:
    file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"🚫 File too large! Please upload a file smaller than {MAX_FILE_SIZE_MB} MB.")
        st.stop()

if uploaded_file:
    try:
        # ---- Only run on first upload ----
        if st.session_state.raw_text is None:
            raw_text = extract_text(uploaded_file)
            st.session_state.raw_text = raw_text

        # ---- Text Preview ----
        with st.expander("📄 Preview the File", expanded=False):
            preview_text = st.session_state.raw_text
            st.text(preview_text[:1000] + "..." if len(preview_text) > 1000 else preview_text)

        # ---- Summary ----
        st.subheader("📝 Auto Summary")
        if st.session_state.summary is None:
            with st.spinner("Summarizing document..."):
                st.session_state.summary = generate_summary(st.session_state.raw_text)
        st.success(st.session_state.summary)
        st.divider()

        # ---- Retriever ----
        if st.session_state.retriever is None:
            with st.spinner("Indexing document for Q&A..."):
                st.session_state.retriever = prepare_retriever(st.session_state.raw_text)


        if st.button("🎯 Generate Challenge Questions"):
            with st.spinner("Generating... Please wait."):
                st.session_state.challenge_questions = generate_challenge_questions(st.session_state.raw_text)
                st.session_state.user_answers = [""] * len(st.session_state.challenge_questions)
                st.session_state.evaluation_results = None
        # Show questions + answer inputs
        if "challenge_questions" in st.session_state:
            for idx, q in enumerate(st.session_state.challenge_questions):
                st.markdown(f"**Q{idx+1}:** {q}")
                st.session_state.user_answers[idx] = st.text_input(
                    f"Your Answer to Q{idx+1}", key=f"challenge_answer_{idx}"
                )

            # Button to evaluate answers
            if st.button("Evaluate My Answers"):
                with st.spinner("Evaluating your responses... It will take a while..."):
                    st.session_state.evaluation_results = evaluate_answers(
                        st.session_state.challenge_questions,
                        st.session_state.user_answers,
                        st.session_state.raw_text
                    )

        # Show evaluation results
        st.divider()
        if "evaluation_results" in st.session_state and st.session_state.evaluation_results:
            st.subheader("✅ Evaluation Results")
            for idx, feedback in enumerate(st.session_state.evaluation_results):
                st.markdown(f"**Feedback for Q{idx+1}:**")
                st.success(feedback)
        
        # ---- Ask Anything: Chat Interface ----
        st.divider()
        st.subheader("💬 Ask Anything Based on the Document")
        user_input = st.chat_input("Type Here... ")

        if user_input:
            # Append only, don't render now
            st.session_state.chat_history.append(("user", user_input))

            with st.spinner("Thinking... Please wait."):
                response = answer_question(user_input, st.session_state.retriever)

                if isinstance(response, dict) and "result" in response:
                    response = response["result"]

                st.session_state.chat_history.append(("assistant", response))

        show_chat()

    except Exception as e:
        st.error(f"❌ Error while processing: {e}")

else:
    st.info("📂 Please upload a PDF or TXT file to begin.")
