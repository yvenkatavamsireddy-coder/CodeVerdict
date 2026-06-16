import subprocess
import tempfile
import os

def run_code(code: str, stdin: str = "", timeout: int = 5):
    # create unique temp file
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
                "timeout", str(timeout),
                "python3", "/app/solution.py"
            ],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout + 2
        )

        if result.returncode == 124:
            return {"verdict": "TLE", "output": None}

        if result.returncode != 0:
            return {"verdict": "RE", "output": result.stderr}

        return {"verdict": "ran", "output": result.stdout.strip()}

    except subprocess.TimeoutExpired:
        return {"verdict": "TLE", "output": None}

    finally:
        os.unlink(filepath)