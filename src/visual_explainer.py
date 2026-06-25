import os
from groq import Groq
from dotenv import load_dotenv
from code_tracer import trace_execution

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)

EXPLAIN_SYSTEM_PROMPT = """You are CodeMentor AI, an expert tutor.
You are given a REAL execution trace of Python code — exact line numbers,
the code on each line, and the EXACT variable values at that moment
(captured by actually running the code, not guessed).

Your job: turn this raw trace into a clear, friendly, step-by-step
explanation a student can follow easily. For each meaningful step,
explain WHAT happened and WHY, referencing the real variable values.

Format your response as a numbered list of steps. Be concise per step
(1-2 sentences) but cover the full execution. Group repetitive loop
iterations sensibly rather than over-explaining identical steps.
"""

def format_trace_for_prompt(trace: list) -> str:
    lines = []
    for step in trace:
        if step.get("event") == "exception":
            lines.append(f"ERROR: {step.get('error')}")
            continue
        vars_str = ", ".join(f"{k}={v}" for k, v in step["variables"].items())
        lines.append(f"Line {step['line_no']}: {step['line_text']}  |  Variables: {vars_str}")
    return "\n".join(lines)

def explain_trace(code: str, topic: str = "") -> dict:
    """
    Run the code, capture real trace, then ask AI to explain it nicely.
    """
    trace, stdout = trace_execution(code)
    trace_text = format_trace_for_prompt(trace)

    user_prompt = f"""Topic: {topic}

Code:
```python
{code}
```

Real execution trace:
{trace_text}

Program output: {stdout}

Explain this execution step by step for a student learning this concept."""

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return {
        "explanation": response.choices[0].message.content,
        "raw_trace": trace,
        "output": stdout
    }

if __name__ == "__main__":
    code = """def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

result = fixed_window([2,1,5,1,3,2], 3)
print(result)
"""

    result = explain_trace(code, topic="Sliding Window")
    print(result["explanation"])
    print(f"\nOutput: {result['output']}")