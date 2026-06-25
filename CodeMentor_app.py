import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from vectorstore import load_vectorstore
from qa_pipeline import ask_question
from auto_fix import run_and_autofix

st.set_page_config(page_title="CodeMentor AI", page_icon="robot", layout="wide")

st.title("CodeMentor AI")
st.caption("Ask Python/DSA questions or run code with AI-powered auto-fix")

@st.cache_resource
def get_vectorstore():
    return load_vectorstore()

vs = get_vectorstore()

tab1, tab2 = st.tabs(["Ask a Question", "Code Runner"])

with tab1:
    st.subheader("Ask anything about Python, DSA, or your own code")

    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    for q, a, sources in st.session_state.qa_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)
            st.caption("Sources: " + ", ".join(sources))

    question = st.chat_input("Ask a question")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking..."):
            answer, sources = ask_question(question, vs)
            source_names = [s.metadata.get("source") for s in sources]

        with st.chat_message("assistant"):
            st.write(answer)
            st.caption("Sources: " + ", ".join(source_names))

        st.session_state.qa_history.append((question, answer, source_names))

with tab2:
    st.subheader("Write Python code, AI explains and fixes errors")

    default_code = "def fixed_window(arr, k):\n    window_sum = sum(arr[:k])\n    max_sum = window_sum\n    for i in range(k, len(arr)):\n        window_sum += arr[i] - arr[i-k]\n        max_sum = max(max_sum, window_sum)\n    return max_sum\n\nprint(fixed_window([2,1,5,1,3,2], 3))"

    code = st.text_area("Your Python code:", value=default_code, height=250)

    if st.button("Run Code", type="primary"):
        with st.spinner("Running your code safely in a sandbox..."):
            result = run_and_autofix(code, vs)

        if result["ran_successfully"]:
            st.success("Code ran successfully!")
            st.code(result["output"], language="text")
        else:
            st.error("Error: " + str(result["error_type"]))
            with st.expander("See raw error"):
                st.code(result["error"], language="text")

            st.subheader("AI Explanation & Fix")
            st.markdown(result["explanation"])