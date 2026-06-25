# CodeMentor AI

An AI-powered coding tutor built from scratch, using my own 135-file Python/DSA codebase as its knowledge base. It teaches programming concepts, lets learners self-test before getting help, executes code in a secure sandbox, and traces real code execution line-by-line.

## Why I Built This

During an AI Intern interview, I was challenged with: "ChatGPT and Claude can already do that. I need someone who knows AI deeply enough to build something beyond a wrapper around an existing model."

This project is my direct answer to that challenge.

## What It Does

1. Learn Mode - browse Python/DSA topics, get theory grounded in my own code, see real execution traces
2. Practice Mode - write your own code or explanation first; AI helps only when you're actually stuck
3. AI Auto-Fix - runs your buggy code in a sandbox, explains the real error, suggests a fix grounded in your notes

## Architecture

135 source files -> Document Loader -> 212 chunks -> AI Classifier -> Topic Catalog (Python / 13 DSA topics / LeetCode) -> FAISS Vector Store (sentence-transformers embeddings) -> Q&A Pipeline + Code Runner + Code Tracer -> Streamlit App (Learn Mode / Practice Mode)

## Key Technical Decisions

- RAG over plain LLM calls: every answer is grounded in my own codebase via FAISS retrieval, reducing hallucination and keeping explanations consistent with how I actually learned each concept.
- Real sandboxed execution, not AI guesses: code runs in an isolated subprocess with a strict CPU time limit. Correct code returns real output; buggy code returns the real traceback; infinite loops are killed automatically.
- sys.settrace() for execution tracing: the visual step-by-step trace feature captures real, line-by-line variable values using Python's introspection tools, not AI-hallucinated guesses.
- AI-powered file classification: a keyword-based pass alone left 75 of 135 files miscategorized. A Groq-based classifier reads each file's actual content and assigns it to the correct topic.
- Self-test-first design: the AI Assistant is not shown by default. The learner attempts their own answer first; AI help appears automatically only when that attempt is wrong.

## Tech Stack

- LLM: Groq (Llama 3.3 70B)
- Vector Store: FAISS
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Frontend: Streamlit
- Execution: Python subprocess + sys.settrace()

## Setup

git clone https://github.com/Manojilango/CodeMentor-Ai.git
cd CodeMentor-Ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run app.py

## Project Structure

src/document_loader.py - reads and chunks the codebase
src/vectorstore.py - FAISS embedding + retrieval
src/qa_pipeline.py - grounded Q&A using retrieved context
src/code_runner.py - sandboxed code execution
src/auto_fix.py - runs buggy code, AI explains and fixes
src/text_evaluator.py - judges if a written explanation is correct
src/ai_classifier.py - AI-powered file topic classification
src/code_tracer.py - real line-by-line execution tracing
src/visual_explainer.py - AI narration of real execution traces
app.py - Streamlit application

## Status

Core features working: grounded Q&A, sandboxed execution, auto-fix, file classification, and execution tracing. Actively being polished.
