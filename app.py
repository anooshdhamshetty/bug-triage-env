from typing import Any, Dict

from fastapi import FastAPI

from env.environment import BugTriageEnv
from env.models import Action
from inference import run_task


app = FastAPI(title="Bug Triage OpenEnv")
env = BugTriageEnv()


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


@app.post("/reset")
@app.post("/openenv/reset")
def reset_env() -> Dict[str, Any]:
    observation = env.reset()
    return {"observation": observation.model_dump()}


@app.post("/step")
@app.post("/openenv/step")
def step_env(action: Action) -> Dict[str, Any]:
    observation, reward, done, info = env.step(action)
    return {
        "observation": observation.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/state")
@app.get("/openenv/state")
def state_env() -> Dict[str, Any]:
    observation = env.state()
    return {"observation": observation.model_dump()}