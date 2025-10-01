# This is my Hydra Skeleton
import logging
from core import model_broker, sandbox

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("🐉 Hydra Orchestrator awakened...")
    # Example: call model broker
    response = model_broker.get_response("Say hello, Hydra!")
    logging.info(f"Model Broker says: {response}")

    # Example: sandbox test
    result = sandbox.run_code("print('Hello from sandbox!')")
    logging.info(f"Sandbox result: {result}")

if __name__ == "__main__":
    main()
