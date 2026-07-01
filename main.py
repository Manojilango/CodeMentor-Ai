from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import ask_question
from src.vectorstore import load_vectorstore

app = FastAPI()

# Load the vectorstore ONCE when the server starts
print("Loading vectorstore...")
vectorstore = load_vectorstore()
print("Vectorstore loaded!")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: QuestionRequest):
    answer, sources = ask_question(request.question, vectorstore)
    return {
        "answer": answer,
        "sources": [s.metadata.get("source") for s in sources]
    }

@app.get("/")
def health_check():
    return {"status": "CodeMentor AI API is running"}
