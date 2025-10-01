# This is my Hydra Skeleton
import logging
from core import model_broker, sandbox, lorekeeper, git_commit_push

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("🐉 Hydra Orchestrator awakened...")

     # Initialize lorekeeper (SQLite)
    lorekeeper.init_db()
    lorekeeper.log_awaken("Hydra has awakened in Docker.")

    # Example: call model broker
    response = model_broker.get_response("Say hello, Hydra!")
    logging.info(f"Model Broker says: {response}")

    # Example: sandbox test
    result = sandbox.run_code("print('Hello from sandbox!')")
    logging.info(f"Sandbox result: {result}")
    
    # Auto-commit & push updated memory
    git_commit_push.commit_push("Hydra updated memory")
if __name__ == "__main__":
    main()
