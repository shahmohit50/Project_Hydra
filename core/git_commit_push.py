import subprocess
import logging

def commit_push(message="Hydra updated memory"):
    """
    Stage all changes, commit with message, and push to GitHub.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        logging.info("📦 Hydra: Auto-commit & push successful")
    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ Hydra: Git operation failed → {e}")
