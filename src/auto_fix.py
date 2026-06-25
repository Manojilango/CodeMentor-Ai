import os
from groq import Groq
from vectorstore import load_vectorstore
from code_runner import run_python_code
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

FIX_SYSTEM_PROMPT = """You are CodeMentor AI, an expert Python and DSA tutor.
A student's code has an error. Your job is to:
1. Explain WHY the error happened, in simple terms
2. Reference relevant concepts from the provided context if helpful
3. Provide the CORRECTED code
4. Briefly explain what you changed and why

Be encouraging and educational, not just a fix dispenser.
Use the context only if it's actually relevant to the bug.
"""

def explain_and_fix(code: str, error_output: str, vectorstore, k: int = 2):
    """
    Given buggy code + its error, retrieve relevant context
    and ask the LLM to explain + fix it.
    """
    # Use the error message to search for relevant context (e.g. similar past bugs/concepts)
    search_query = f"{error_output[:200]}"
    results = vectorstore.similarity_search(search_query, k=k)
    context = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source')}\n{doc.page_content[:300]}"
        for doc in results
    )

    user_prompt = f"""Student's code:
```python
{code}
```

Error output:
{error_output}

Possibly relevant context from student's notes:
{context}

Please explain the bug and provide corrected code."""

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": FIX_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def run_and_autofix(code: str, vectorstore):
    """
    Full pipeline: run code -> if error -> explain and fix -> return everything
    """
    result = run_python_code(code)

    if result["success"]:
        return {
            "ran_successfully": True,
            "output": result["stdout"],
            "explanation": None
        }
    else:
        explanation = explain_and_fix(code, result["stderr"], vectorstore)
        return {
            "ran_successfully": False,
            "output": result["stdout"],
            "error": result["stderr"],
            "error_type": result["error_type"],
            "explanation": explanation
        }

if __name__ == "__main__":
    print("Loading vectorstore...")
    vs = load_vectorstore()

    buggy_code = """
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

print(fixed_window([2,1,5,1,3,2], "3"))
"""

    print("\n=== Running buggy code through auto-fix pipeline ===\n")
    result = run_and_autofix(buggy_code, vs)

    print(f"Ran successfully: {result['ran_successfully']}")
    if not result['ran_successfully']:
        print(f"\nError type: {result['error_type']}")
        print(f"\n--- AI Explanation & Fix ---\n")
        print(result['explanation'])
