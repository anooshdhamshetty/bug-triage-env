import json
import os
import random
from typing import List, Optional, Tuple

from openai import OpenAI

from env.environment import BugTriageEnv
from env.models import Action
from graders.grader import evaluate


IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("API_KEY") or os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.groq.com/openai/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "llama-3.3-70b-versatile"
BENCHMARK = os.getenv("BENCHMARK", "bug-triage-env")
MAX_STEPS = 3

LEGACY_GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def resolve_api_base_url(raw_url: str) -> str:
    normalized = raw_url.strip().rstrip("/")
    if normalized != LEGACY_GROQ_BASE_URL.rstrip("/"):
        print(
            "[WARN] API_BASE_URL is not set to Groq's OpenAI-compatible endpoint; using the provided value as-is",
            flush=True,
        )
    return normalized

if not API_KEY:
    raise Exception(
        "Missing required environment variable: GROQ_API_KEY. Set it in your shell or add it as a Secret in your Hugging Face Space settings before starting the app."
    )

API_BASE_URL = resolve_api_base_url(API_BASE_URL)
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


def build_prompt(observation, step: int) -> str:
    base = f"""
You are a bug triage agent.

Bug Report:
Title: {observation.title}
Description: {observation.description}
Logs: {observation.logs}
User Impact: {observation.user_impact}
Frequency: {observation.frequency}

IMPORTANT:
- Respond ONLY with valid JSON
- No explanation
"""
    if step == 0:
        return base + '\n{"category": "ui/backend/database/network"}'
    if step == 1:
        return base + '\n{"severity": "low/medium/high"}'
    return base + '\n{"team": "frontend_team/backend_team/payments_team/infra_team"}'


def call_model(prompt: str) -> Tuple[str, Optional[str]]:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content
        return (content.strip() if content else "{}", None)
    except Exception as exc:
        return ("{}", str(exc))


def parse_response(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except Exception:
            return {}


def normalize(value: Optional[str], allowed: List[str], default: str) -> str:
    if value is None:
        return default
    value = str(value).lower().strip()
    for item in allowed:
        if item in value:
            return item
    return default


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    done_val = str(done).lower()
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{reward:.2f}" for reward in rewards)
    success_val = str(success).lower()
    print(f"[END] success={success_val} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def run_task(task_name: str) -> float:
    env = BugTriageEnv()
    observation = env.reset()
    prediction = {}
    rewards: List[float] = []
    step_count = 0
    done = False
    task_error = None

    log_start(task_name, BENCHMARK, MODEL_NAME)

    try:
        prompt = build_prompt(observation, 0)
        raw_output, last_error = call_model(prompt)
        parsed = parse_response(raw_output)
        category = normalize(parsed.get("category"), ["ui", "backend", "database", "network"], "backend")
        observation, reward, done, _ = env.step(Action(category=category))
        prediction["category"] = category
        rewards.append(reward)
        step_count += 1
        log_step(step_count, f"category={category}", reward, done, last_error)

        if not done and step_count < MAX_STEPS:
            prompt = build_prompt(observation, 1)
            raw_output, last_error = call_model(prompt)
            parsed = parse_response(raw_output)
            severity = normalize(parsed.get("severity"), ["low", "medium", "high"], "medium")
            observation, reward, done, _ = env.step(Action(severity=severity))
            prediction["severity"] = severity
            rewards.append(reward)
            step_count += 1
            log_step(step_count, f"severity={severity}", reward, done, last_error)

        if not done and step_count < MAX_STEPS:
            prompt = build_prompt(observation, 2)
            raw_output, last_error = call_model(prompt)
            parsed = parse_response(raw_output)
            team = normalize(
                parsed.get("team"),
                ["frontend_team", "backend_team", "payments_team", "infra_team"],
                "backend_team",
            )
            observation, reward, done, _ = env.step(Action(team=team))
            prediction["team"] = team
            rewards.append(reward)
            step_count += 1
            log_step(step_count, f"team={team}", reward, done, last_error)

    except Exception as exc:
        task_error = str(exc)
        log_step(step_count + 1, "exception", 0.00, True, task_error)

    expected = env.current_bug["expected"]
    score = evaluate(task_name, prediction, expected)
    success = bool(score >= 0.5 and task_error is None)
    log_end(success, step_count, score, rewards)
    return score


if __name__ == "__main__":
    random.seed(42)
    tasks = ["easy", "medium", "hard"]
    for task in tasks:
        run_task(task)