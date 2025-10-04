import os, json, logging
from datetime import datetime
from pathlib import Path
from core import lorekeeper, model_broker

OUTDIR = Path("output") / "code_forger"
OUTDIR.mkdir(parents=True, exist_ok=True)

class CodeForger:
    async def run(self, payload: dict) -> dict:
        language = payload.get("language", "python")
        desc = payload.get("description", "small demo")
        prompt = f"Create a {language} project: {desc} -- give files and structure"

        # generated = await model_broker.broker.query(prompt)
        generated = model_broker.broker.load("mistral:7b-instruct-v0.2-q4_K_M",prompt)

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = OUTDIR / f"{payload.get('project_name','project')}-{timestamp}.json"
        data = {"language": language, "description": desc, "output": generated, "created_at": timestamp}
        filename.write_text(json.dumps(data, indent=2))

        lorekeeper.log_awaken(f"CodeForger generated: {payload.get('project_name','project')}")
        logging.info(f"CodeForger: wrote {filename}")
        return {"status": "done", "path": str(filename)}
