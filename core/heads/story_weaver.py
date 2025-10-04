import os, json, logging
from datetime import datetime
from pathlib import Path
from core import lorekeeper, model_broker

OUTDIR = Path("output") / "story_weaver"
OUTDIR.mkdir(parents=True, exist_ok=True)

class StoryWeaver:
    async def run(self, payload: dict) -> dict:
        title = payload.get("title", "untitled")
        prompt = payload.get("input", f"Write a short scene titled {title}")

        # generated = await model_broker.broker.query(prompt)
        # generated = await model_broker.broker.query(prompt, model="mistral")
        generated = model_broker.broker.load("mistral:7b-instruct-v0.2-q4_K_M",prompt)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = OUTDIR / f"{title.replace(' ','_')}-{timestamp}.json"
        data = {"title": title, "prompt": prompt, "output": generated, "created_at": timestamp}
        filename.write_text(json.dumps(data, indent=2))

        lorekeeper.log_awaken(f"StoryWeaver produced: {title}")
        logging.info(f"StoryWeaver: wrote {filename}")
        return {"status": "done", "path": str(filename)}
