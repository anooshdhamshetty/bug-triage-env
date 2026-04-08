---
title: Bug Triage OpenEnv Environment
emoji: 🐛
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Bug Triage OpenEnv Environment

This project implements a real-world bug triage environment where an agent must classify a bug report into:

- `category`: `ui | backend | database | network`
- `severity`: `low | medium | high`
- `team`: `frontend_team | backend_team | payments_team | infra_team`

The environment is intended for OpenEnv-style agent evaluation and includes three tasks (`easy`, `medium`, `hard`) with deterministic graders.

## Environment Design

- Observation model (`env/models.py`):
	- `title: str`
	- `description: str`
	- `logs: str`
	- `user_impact: str`
	- `frequency: int`
	- `module_hint: Optional[str]`
- Action model (`env/models.py`):
	- `category: Optional[str]`
	- `severity: Optional[str]`
	- `team: Optional[str]`

### Episode Flow

The environment runs exactly 3 steps:

1. Predict category
2. Predict severity
3. Predict routing team

Reward shaping (`env/environment.py`):

- Step 1 category: `+0.3` if correct, `-0.2` if incorrect
- Step 2 severity: `+0.3` if correct, `-0.2` if incorrect
- Step 3 team: `+0.4` if correct, `-0.2` if incorrect

Total reward is clipped to `[0.0, 1.0]`.

## Tasks and Graders

- `easy`: score only category correctness (`0.0` or `1.0`)
- `medium`: score category + severity (`0.0`, `0.5`, `1.0`)
- `hard`: full triage weighted score in `[0.0, 1.0]`

Grader implementation: `graders/grader.py`.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Required environment variables:

- `GROQ_API_KEY`
- `API_BASE_URL`
- `MODEL_NAME`

If you deploy this as a Hugging Face Space, add `GROQ_API_KEY` under Space settings -> Secrets. The app will fail to start until that secret is present.

Optional:

- `BENCHMARK` (default: `bug-triage-env`)

## Run Baseline Inference

```bash
python inference.py
```

The script emits strictly formatted logs:

- `[START] task=<task_name> env=<benchmark> model=<model_name>`
- `[STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>`
- `[END] success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>`

and computes a final average score across `easy`, `medium`, and `hard`.

Groq defaults:

- `API_BASE_URL=https://api.groq.com/openai/v1`
- `MODEL_NAME=llama-3.1-70b-versatile`

## Docker

Build and run:

```bash
docker build -t bug-triage-env .
docker run --rm -e GROQ_API_KEY=<token> -e API_BASE_URL=<url> -e MODEL_NAME=<model> bug-triage-env
```

## Project Structure

- `env/`: environment logic, models, scoring and signal extraction
- `data/`: synthetic bug dataset with expected outputs
- `tasks/`: task wrappers for easy/medium/hard
- `graders/`: deterministic grading logic
- `inference.py`: baseline model loop using OpenAI client
- `openenv.yaml`: metadata and action/observation schema
