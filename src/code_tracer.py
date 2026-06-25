import sys
import io
import contextlib

def trace_execution(code: str, max_steps: int = 50) -> list:
    trace_log = []
    code_lines = code.split('\n')
    code_filename = "<user_code>"

    # Compile the code so we can check the filename in trace frames
    compiled_code = compile(code, code_filename, 'exec')

    def tracer(frame, event, arg):
        # Only trace lines that belong to the USER'S code, not internal Python machinery
        if frame.f_code.co_filename != code_filename:
            return None

        if event == 'line':
            line_no = frame.f_lineno
            local_vars = {
                k: repr(v)[:100]
                for k, v in frame.f_locals.items()
                if not k.startswith('__')
            }
            line_text = code_lines[line_no - 1].strip() if line_no <= len(code_lines) else ""

            trace_log.append({
                "line_no": line_no,
                "line_text": line_text,
                "variables": local_vars,
                "event": event
            })

            if len(trace_log) >= max_steps:
                sys.settrace(None)

        return tracer

    output_buffer = io.StringIO()
    exec_globals = {}

    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(output_buffer):
            exec(compiled_code, exec_globals)
    except Exception as e:
        trace_log.append({
            "line_no": -1,
            "line_text": "ERROR",
            "variables": {},
            "event": "exception",
            "error": str(e)
        })
    finally:
        sys.settrace(None)

    return trace_log, output_buffer.getvalue()

if __name__ == "__main__":
    test_code = """def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

result = fixed_window([2,1,5,1,3,2], 3)
print(result)
"""

    trace, stdout = trace_execution(test_code)

    print(f"Captured {len(trace)} steps\n")
    for step in trace:
        print(f"Line {step['line_no']}: {step['line_text']}")
        print(f"  Variables: {step['variables']}")
        print()

    print(f"Output: {stdout}")