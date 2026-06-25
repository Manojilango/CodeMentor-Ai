import subprocess
import tempfile
import os
import platform

TIMEOUT_SECONDS = 5

def set_cpu_limit():
    """Set CPU time limit for the subprocess (Unix only, macOS-safe)"""
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS))

def run_python_code(code: str) -> dict:
    """
    Safely execute Python code in a sandboxed subprocess.
    Returns dict with: success, stdout, stderr, error_type
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name

    try:
        # Only apply preexec_fn on Unix (Linux/macOS), and only CPU limit (memory limit breaks on macOS)
        preexec = set_cpu_limit if platform.system() != "Windows" else None

        result = subprocess.run(
            ['python3', temp_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            preexec_fn=preexec
        )

        success = result.returncode == 0

        return {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error_type": None if success else classify_error(result.stderr),
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {TIMEOUT_SECONDS} seconds (possible infinite loop)",
            "error_type": "TimeoutError",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "error_type": "ExecutionError",
            "exit_code": -1
        }
    finally:
        os.unlink(temp_path)

def classify_error(stderr: str) -> str:
    """Extract the error type from Python traceback"""
    lines = stderr.strip().split('\n')
    if lines:
        last_line = lines[-1]
        if ':' in last_line:
            return last_line.split(':')[0].strip()
    return "UnknownError"

if __name__ == "__main__":
    print("=== Test 1: Correct code ===")
    code1 = """
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

print(fixed_window([2,1,5,1,3,2], 3))
"""
    result1 = run_python_code(code1)
    print(result1)

    print("\n=== Test 2: Buggy code ===")
    code2 = """
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

print(fixed_window([2,1,5,1,3,2], "3"))
"""
    result2 = run_python_code(code2)
    print(result2)

    print("\n=== Test 3: Infinite loop ===")
    code3 = """
while True:
    pass
"""
    result3 = run_python_code(code3)
    print(result3)
