import os
from groq import Groq
from vectorstore import load_vectorstore
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file!")
    return Groq(api_key=api_key)

SYSTEM_PROMPT = """You are CodeMentor AI, an expert Python and DSA tutor.
You answer questions using ONLY the provided context from the student's own code and notes.

Rules:
- Explain concepts clearly and simply, like teaching a student
- Reference the actual code in the context when relevant
- If the context doesn't contain enough info, say so honestly
- Use simple language, avoid unnecessary jargon
- When explaining code, go line by line if helpful
"""

def ask_question(question: str, vectorstore, k: int = 3):
    # Retrieve relevant chunks
    results = vectorstore.similarity_search(question, k=k)
    context = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
        for doc in results
    )

    # Build prompt
    user_prompt = f"""Context from student's code/notes:
{context}

Question: {question}

Answer the question using the context above."""

    # Call Groq
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content, results

if __name__ == "__main__":
    print("Loading vectorstore...")
    vs = load_vectorstore()

    questions = [
        "What is sliding window and how does it work?",
        "Explain two pointers technique",
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        print(f"{'='*60}")
        answer, sources = ask_question(q, vs)
        print(f"\nAnswer:\n{answer}")
        print(f"\nSources used: {[s.metadata.get('source') for s in sources]}")
