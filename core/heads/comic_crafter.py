import os, json, logging
from datetime import datetime
from pathlib import Path
from core import lorekeeper, model_broker

OUTDIR = Path("output") / "comic_crafter"
OUTDIR.mkdir(parents=True, exist_ok=True)

class ComicCrafter:
    async def run(self, payload: dict) -> dict:
        scene = payload.get("scene", "A hero walks into a dark temple")
        prompt = f"Generate comic panel prompts for: {scene}"

        # generated = await model_broker.broker.query(prompt)
        generated = model_broker.broker.load("mistral:7b-instruct-v0.2-q4_K_M",prompt)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = OUTDIR / f"comic-{timestamp}.json"
        filename.write_text(json.dumps({"scene": scene, "panels": generated, "created_at": timestamp}, indent=2))

        lorekeeper.log_awaken("ComicCrafter sketched a scene")
        logging.info(f"ComicCrafter: wrote {filename}")
        return {"status": "done", "path": str(filename)}
