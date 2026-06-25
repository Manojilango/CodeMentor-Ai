import os
import json
import time
from topic_organizer import categorize_files
from ai_classifier import classify_file

def build_catalog():
    folder = os.path.expanduser("~/CodeMentor-AI/data/Coding-solving-")
    result = categorize_files(folder)

    catalog = {"Python": result["Python"], "DSA": result["DSA"], "LeetCode": []}

    print(f"Classifying {len(result['LeetCode'])} uncategorized files with AI...")

    category_map = {
        "PYTHON_BASICS": ("Python", None),
        "DSA_TWO_POINTERS": ("DSA", "Two Pointers"),
        "DSA_SLIDING_WINDOW": ("DSA", "Sliding Window"),
        "DSA_BINARY_SEARCH": ("DSA", "Binary Search"),
        "DSA_STACK": ("DSA", "Stack"),
        "DSA_LINKED_LIST": ("DSA", "Linked List"),
        "DSA_TREES": ("DSA", "Trees BFS/DFS"),
        "DSA_GRAPHS": ("DSA", "Graphs"),
        "DSA_DP": ("DSA", "Dynamic Programming"),
        "DSA_BACKTRACKING": ("DSA", "Backtracking"),
        "DSA_GREEDY": ("DSA", "Greedy"),
        "DSA_HEAP": ("DSA", "Heap"),
        "DSA_HASHMAP": ("DSA", "Hashmap"),
        "DSA_MONOTONIC_STACK": ("DSA", "Monotonic Stack"),
        "LEETCODE_OTHER": ("LeetCode", None),
        "IGNORE": (None, None),
    }

    for i, filepath in enumerate(result["LeetCode"]):
        category = classify_file(filepath)
        bucket, subtopic = category_map.get(category, ("LeetCode", None))

        if bucket is None:
            continue  # IGNORE
        elif bucket == "Python":
            catalog["Python"].append(filepath)
        elif bucket == "DSA":
            catalog["DSA"].setdefault(subtopic, []).append(filepath)
        else:
            catalog["LeetCode"].append(filepath)

        print(f"  [{i+1}/{len(result['LeetCode'])}] {os.path.basename(filepath)} → {category}")
        time.sleep(0.3)  # avoid rate limits

    # Save catalog to JSON for reuse in the app
    catalog_serializable = {
        "Python": catalog["Python"],
        "DSA": catalog["DSA"],
        "LeetCode": catalog["LeetCode"]
    }

    save_path = os.path.expanduser("~/CodeMentor-AI/data/catalog.json")
    with open(save_path, 'w') as f:
        json.dump(catalog_serializable, f, indent=2)

    print(f"\nCatalog saved to {save_path}")
    print(f"\nFinal counts:")
    print(f"  Python: {len(catalog['Python'])}")
    for topic, files in catalog["DSA"].items():
        print(f"  DSA - {topic}: {len(files)}")
    print(f"  LeetCode (other): {len(catalog['LeetCode'])}")

    return catalog

if __name__ == "__main__":
    build_catalog()
