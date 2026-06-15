import subprocess
import tempfile
import os

def run_code(code: str, stdin: str = ""):
    # create a unique temp file for each submission
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        filepath = f.name

    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "--memory", "128m",
                "--cpus", "0.5",
                "-i",
                "-v", f"{filepath}:/app/solution.py",
                "python:3.11-slim",
                "timeout", "5",
                "python3", "/app/solution.py"
            ],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result

    finally:
        os.unlink(filepath)  # always delete temp file even if something crashes

def judge(code: str, test_cases: list):
    for tc in test_cases:
        result = run_code(code, tc["input"])

        if result.returncode == 124:
            return "TLE"

        if result.returncode != 0:
            return "RE"

        if result.stdout.strip() != tc["expected_output"].strip():
            return "WA"

    return "AC"


# test it
code = """
n = int(input())
print(n * 2)
"""

test_cases = [
    {"input": "5", "expected_output": "10"},
    {"input": "3", "expected_output": "6"},
    {"input": "0", "expected_output": "0"},
]

print(judge(code, test_cases))