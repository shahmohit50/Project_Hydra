import subprocess

def run_code(code: str) -> str:
    """
    Runs Python code safely (very basic placeholder).
    Later this will execute inside an isolated sandbox.
    """
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() if result.stdout else result.stderr.strip()
    except Exception as e:
        return f"Sandbox error: {e}"
