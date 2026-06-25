import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

CLASSIFY_SYSTEM_PROMPT = """You classify Python code files into exactly one category.

Categories:
- PYTHON_BASICS: general Python syntax practice (loops, OOP, libraries like pandas/matplotlib/numpy basics, not a DSA algorithm)
- DSA_TWO_POINTERS, DSA_SLIDING_WINDOW, DSA_BINARY_SEARCH, DSA_STACK, DSA_LINKED_LIST,
  DSA_TREES, DSA_GRAPHS, DSA_DP, DSA_BACKTRACKING, DSA_GREEDY, DSA_HEAP, DSA_HASHMAP, DSA_MONOTONIC_STACK
  (specific DSA pattern, if the code clearly implements one of these algorithms)
- LEETCODE_OTHER: a leetcode-style coding problem that doesn't clearly fit the above patterns
- IGNORE: junk/empty/irrelevant file, or unrelated AI/ML project code (RAG, ML models, etc.)

Respond with ONLY the category name, nothing else."""

def classify_file(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return "IGNORE"

    if not content.strip() or len(content) < 20:
        return "IGNORE"

    # Use only first 600 chars to keep it fast/cheap
    snippet = content[:600]

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": CLASSIFY_SYSTEM_PROMPT},
            {"role": "user", "content": f"Filename: {os.path.basename(filepath)}\n\nCode:\n{snippet}"}
        ],
        temperature=0.0,
        max_tokens=20
    )

    category = response.choices[0].message.content.strip()
    return category

if __name__ == "__main__":
    # Quick test on a few files
    test_files = [
        "search_2d_matrix.py",
        "matplotlib_basics.py",
        "top_k_frequent.py",
        "filename.py"
    ]

    folder = os.path.expanduser("~/CodeMentor-AI/data/Coding-solving-")

    for root, dirs, files in os.walk(folder):
        for f in files:
            if f in test_files:
                full_path = os.path.join(root, f)
                category = classify_file(full_path)
                print(f"{f} → {category}")
