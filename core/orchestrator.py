# This is my Hydra Skeleton
import logging, asyncio
from core import model_broker, sandbox, lorekeeper, git_commit_push
from core.heads import HEAD_REGISTRY

logging.basicConfig(level=logging.INFO)

async def run_head(head_name: str, payload: dict):
    head_cls = HEAD_REGISTRY.get(head_name)
    if not head_cls:
        logging.error(f"No such head: {head_name}")
        return {"status":"rejected","reason":"unknown head"}
    head = head_cls()
    return await head.run(payload)

async def main_async():
    logging.info("🐉 Hydra Orchestrator awakened...")

     # Initialize lorekeeper (SQLite)
    lorekeeper.init_db()
    lorekeeper.log_awaken("Hydra has awakened in Docker.")

    # Example: call model broker
    response = model_broker.broker.load("mistral:7b-instruct-v0.2-q4_K_M","Say hello, Hydra!")
    logging.info(f"Model Broker says: {response}")

    tasks = [
        run_head("story_weaver", {"title":"FirstScene","input":"Dark lord rises..."}),
        run_head("code_forger", {"language":"python","description":"CLI hello","project_name":"greet_cli"})
    ]
    results = await asyncio.gather(*tasks)
    logging.info(f"Head results: {results}")

    # Example: sandbox test
    result = sandbox.run_code("print('Hello from sandbox!')")
    logging.info(f"Sandbox result: {result}")

    # Auto-commit & push updated memory
    git_commit_push.commit_push("Hydra updated memory")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
