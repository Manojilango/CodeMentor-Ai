import os
import re

# Files/keywords to EXCLUDE entirely (AI/ML project files, not coding problems)
EXCLUDE_KEYWORDS = [
    "rag", "xgboost", "titanic", "linear_regression", "random_forest",
    "ml_pipeline", "decision_tree", "logistic_regression", "lang",
    "streamlit", "chromadb", "sklearn", "model", "groq", "app.py"
]

DSA_KEYWORDS = {
    "Two Pointers": ["two_pointer", "twopointer", "two_sum", "twosum", "reverse_array"],
    "Sliding Window": ["sliding_window", "slide"],
    "Binary Search": ["binary_search"],
    "Stack": ["stack", "parenthes"],
    "Linked List": ["linked_list", "linkedlist"],
    "Trees BFS/DFS": ["bfs", "dfs", "tree", "level_order"],
    "Graphs": ["graph", "islands"],
    "Dynamic Programming": ["dp", "climbing_stair", "house_robber", "coin_change", "unique_paths", "partition", "lis", "palindrome"],
    "Backtracking": ["backtrack", "permutation", "combination", "subset", "word_search"],
    "Greedy": ["greedy", "jump_game", "interval", "merge_intervals", "insert_interval"],
    "Heap": ["heap", "kth_largest"],
    "Hashmap": ["hashmap", "frequency", "anagram", "duplicate"],
    "Monotonic Stack": ["next_greater", "daily_temp", "monotonic"],
}

PYTHON_BASICS_KEYWORDS = [
    "week", "oop", "dict_revision", "list_revision", "loop", "class_animal",
    "inheritance", "big_o", "dsa_day"
]

def should_exclude(filename_lower):
    return any(kw in filename_lower for kw in EXCLUDE_KEYWORDS)

def categorize_files(folder_path):
    categories = {"Python": [], "DSA": {}, "LeetCode": []}

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
        for file in files:
            if not file.endswith('.py'):
                continue

            filepath = os.path.join(root, file)
            filename_lower = file.lower()

            # Skip excluded AI/ML files
            if should_exclude(filename_lower):
                continue

            # Check DSA topics first
            matched_topic = None
            for topic, keywords in DSA_KEYWORDS.items():
                if any(kw in filename_lower for kw in keywords):
                    matched_topic = topic
                    break

            if matched_topic:
                categories["DSA"].setdefault(matched_topic, []).append(filepath)
            elif any(kw in filename_lower for kw in PYTHON_BASICS_KEYWORDS):
                categories["Python"].append(filepath)
            else:
                # Remaining files = likely LeetCode-style problems
                categories["LeetCode"].append(filepath)

    return categories

if __name__ == "__main__":
    folder = os.path.expanduser("~/CodeMentor-AI/data/Coding-solving-")
    result = categorize_files(folder)

    print(f"Python files: {len(result['Python'])}")
    print(f"\nDSA topics found:")
    total_dsa = 0
    for topic, files in result["DSA"].items():
        print(f"  {topic}: {len(files)} files")
        total_dsa += len(files)
    print(f"  TOTAL DSA: {total_dsa}")

    print(f"\nLeetCode files: {len(result['LeetCode'])}")
    print("Sample LeetCode filenames:")
    for f in result["LeetCode"][:20]:
        print(f"  - {os.path.basename(f)}")
