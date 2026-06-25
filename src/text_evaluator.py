import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

EVAL_SYSTEM_PROMPT = """You are an expert Python/DSA tutor evaluating a student's explanation.

Given a TOPIC and the STUDENT'S EXPLANATION, judge if their understanding is correct.

Respond in this exact format:
VERDICT: CORRECT or INCORRECT or PARTIALLY_CORRECT
FEEDBACK: (1-2 sentences on what they got right or missed)

Be encouraging but honest. Minor wording differences are fine if the core concept is right.
"""

def evaluate_text_answer(topic: str, student_answer: str, context: str = "") -> dict:
    user_prompt = f"""Topic: {topic}

Relevant context (if helpful):
{context}

Student's explanation:
{student_answer}

Evaluate this explanation."""

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EVAL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content

    verdict = "INCORRECT"
    feedback = raw

    if "VERDICT:" in raw:
        lines = raw.split("\n")
        for line in lines:
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            if line.startswith("FEEDBACK:"):
                feedback = line.replace("FEEDBACK:", "").strip()

    return {
        "verdict": verdict,
        "feedback": feedback,
        "is_correct": verdict.upper() == "CORRECT"
    }

if __name__ == "__main__":
    # Test 1: Good answer
    result1 = evaluate_text_answer(
        "What is a Hashmap?",
        "A hashmap stores key-value pairs and allows O(1) lookup time using a hash function to map keys to array indices."
    )
    print("Test 1 (good answer):", result1)

    # Test 2: Wrong answer
    result2 = evaluate_text_answer(
        "What is a Hashmap?",
        "A hashmap is a type of array that stores numbers in order."
    )
    print("\nTest 2 (wrong answer):", result2)
