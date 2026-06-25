import streamlit as st
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from vectorstore import load_vectorstore
from qa_pipeline import ask_question
from auto_fix import run_and_autofix
from text_evaluator import evaluate_text_answer
from code_runner import run_python_code
from visual_explainer import explain_trace

st.set_page_config(page_title="CodeMentor AI", page_icon="robot", layout="wide")

@st.cache_resource
def get_vectorstore():
    return load_vectorstore()

@st.cache_data
def load_catalog():
    path = os.path.expanduser("~/CodeMentor-AI/data/catalog.json")
    with open(path, 'r') as f:
        return json.load(f)

vs = get_vectorstore()
catalog = load_catalog()

st.title("CodeMentor AI")
st.caption("Learn topics with theory + visual traces. Practice and get AI help when stuck.")

page = st.sidebar.radio("Mode", ["Learn", "Practice"])

st.sidebar.divider()
st.sidebar.subheader("Browse Topics")

search_query = st.sidebar.text_input("Search any topic:")

st.sidebar.markdown("**DSA Topics:**")
for topic_name, files in catalog["DSA"].items():
    if st.sidebar.button(f"{topic_name} ({len(files)})", key=f"dsa_{topic_name}"):
        st.session_state.selected_topic = topic_name
        st.session_state.selected_files = files

st.sidebar.markdown("**Other:**")
if st.sidebar.button(f"Python Basics ({len(catalog['Python'])})"):
    st.session_state.selected_topic = "Python Basics"
    st.session_state.selected_files = catalog["Python"]

if st.sidebar.button(f"LeetCode Problems ({len(catalog['LeetCode'])})"):
    st.session_state.selected_topic = "LeetCode Problems"
    st.session_state.selected_files = catalog["LeetCode"]

active_topic = search_query if search_query else st.session_state.get("selected_topic", None)

# ---------------- LEARN MODE ----------------
if page == "Learn":
    st.subheader("Learn Mode")

    if active_topic:
        st.markdown(f"## {active_topic}")

        # SECTION 1 — THEORY
        st.markdown("### 1. Theory")
        with st.spinner("Loading explanation..."):
            answer, sources = ask_question(
                f"Explain {active_topic} clearly with a real-life analogy, in 4-6 sentences.",
                vs
            )
            source_names = [s.metadata.get("source") for s in sources]
        st.markdown(answer)
        st.caption("Sources: " + ", ".join(source_names))

        st.divider()

        # SECTION 2 — EXAMPLE CODE
        st.markdown("### 2. Example Code")

        example_code = None
        if st.session_state.get("selected_files"):
            first_file = st.session_state.selected_files[0]
            try:
                with open(first_file, 'r') as f:
                    example_code = f.read()
            except Exception:
                example_code = None

        if not example_code:
            with st.spinner("Generating example code..."):
                code_answer, _ = ask_question(
                    f"Give a short, clean, runnable Python example demonstrating {active_topic}. Only output the code in a code block.",
                    vs
                )
                example_code = code_answer

        st.code(example_code, language="python")

        with st.expander("Debug: Raw example code"):
            st.text(repr(example_code))
            # Also save to a file so we can inspect it via terminal
            with open(os.path.expanduser("~/CodeMentor-AI/debug_output.txt"), "w") as debug_f:
                debug_f.write(example_code)

        st.divider()

        # SECTION 3 — VISUAL STEP-BY-STEP TRACE

        # SECTION 3 — VISUAL STEP-BY-STEP TRACE
        st.markdown("### 3. Visual Step-by-Step Trace")

        if st.button("Generate Visual Trace"):
            with st.spinner("Running code and tracing execution..."):
                try:
                    trace_result = explain_trace(example_code, topic=active_topic)
                    st.markdown(trace_result["explanation"])
                    st.success(f"Program Output: {trace_result['output']}")
                except Exception as e:
                    st.error(f"Could not trace this code automatically: {e}")
                    st.info("Try the 'Write code' option in Practice Mode instead.")

    else:
        st.info("Select a topic from the sidebar or search for one to start learning.")

# ---------------- PRACTICE MODE ----------------
else:
    st.subheader("Practice Mode")

    topic = st.text_input("Topic to practice:", value=active_topic or "")

    mode = st.radio("Answer type:", ["Explain in words", "Write code"], horizontal=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if topic:
            if mode == "Explain in words":
                student_answer = st.text_area("Your explanation:", height=150)

                if st.button("Check My Answer", type="primary"):
                    with st.spinner("Checking..."):
                        results = vs.similarity_search(topic, k=2)
                        context = "\n".join(d.page_content[:300] for d in results)
                        eval_result = evaluate_text_answer(topic, student_answer, context)

                    if eval_result["is_correct"]:
                        st.success(f"Correct! {eval_result['feedback']}")
                    else:
                        st.error(f"Not quite. {eval_result['feedback']}")
                        st.session_state.needs_help = True
                        st.session_state.help_topic = topic

            else:
                student_code = st.text_area("Your code:", value="# Write your code here\n", height=250)

                if st.button("Run & Check My Code", type="primary"):
                    with st.spinner("Running..."):
                        result = run_python_code(student_code)

                    if result["success"]:
                        st.success("Code ran successfully!")
                        st.code(result["stdout"], language="text")

                        if st.button("Show Visual Trace"):
                            with st.spinner("Generating trace..."):
                                trace_result = explain_trace(student_code, topic=topic)
                                st.markdown(trace_result["explanation"])
                    else:
                        st.error(f"Error: {result['error_type']}")
                        with st.expander("Raw error"):
                            st.code(result["stderr"], language="text")
                        st.session_state.needs_help = True
                        st.session_state.help_topic = topic
                        st.session_state.help_code = student_code

    with col2:
        st.markdown("**AI Assistant**")
        if st.button("Ask AI Assistant"):
            st.session_state.needs_help = True
            st.session_state.help_topic = topic

        if st.session_state.get("needs_help"):
            with st.spinner("Thinking..."):
                if st.session_state.get("help_code"):
                    fix_result = run_and_autofix(st.session_state.help_code, vs)
                    st.markdown(fix_result["explanation"])
                else:
                    answer, sources = ask_question(st.session_state.get("help_topic", topic), vs)
                    st.markdown(answer)