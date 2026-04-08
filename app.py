import json
from typing import Dict

from fastapi import FastAPI

from inference import run_task


app = FastAPI(title="Bug Triage OpenEnv")


@app.get("/")
def home() -> Dict[str, str]:
    return {
        "status": "ok",
        "message": "Bug Triage OpenEnv is running.",
        "run_endpoint": "/run",
    }


@app.get("/run")
def run_all_tasks() -> Dict[str, float]:
    results: Dict[str, float] = {}
    for task_name in ["easy", "medium", "hard"]:
        results[task_name] = run_task(task_name)
    return results