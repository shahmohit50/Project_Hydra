import os, json, logging
from datetime import datetime
from pathlib import Path
from core import lorekeeper, model_broker

OUTDIR = Path("output") / "story_transformer"
OUTDIR.mkdir(parents=True, exist_ok=True)

class StoryTransformer:
    async def run(self, payload: dict) -> dict:
        # payload: {"existing_story": "...", "target_style": "Indian", "preserve": ["characters","tone"]}
        story = payload.get("existing_story", "")
        style = payload.get("target_style", "Western")
        preserve = payload.get("preserve", ["characters","tone"])

        prompt = f"Transform this story into {style} fantasy while preserving {', '.join(preserve)}:\n{story}"

        # generated = await model_broker.broker.query(prompt)
        # generated = await model_broker.broker.query(prompt, model="groq")
        generated = model_broker.broker.load("llama-3-70b",prompt)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = OUTDIR / f"transformed-{timestamp}.json"
        data = {"input_story": story, "target_style": style, "output": generated, "created_at": timestamp}
        filename.write_text(json.dumps(data, indent=2))

        lorekeeper.log_awaken(f"StoryTransformer transformed story to {style}")
        logging.info(f"StoryTransformer: wrote {filename}")
        return {"status": "done", "path": str(filename)}
