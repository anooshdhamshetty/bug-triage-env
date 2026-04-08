from pydantic import BaseModel, Field
from typing import Optional


# =========================
# Observation Model
# =========================
class Observation(BaseModel):
    title: str
    description: str
    logs: str
    user_impact: str  # "low", "medium", "high"
    frequency: int
    module_hint: Optional[str] = ""


# =========================
# Action Model
# =========================
class Action(BaseModel):
    # We keep all optional because of multi-step RL
    category: Optional[str] = None
    severity: Optional[str] = None
    team: Optional[str] = None


# =========================
# Reward Model
# =========================
class Reward(BaseModel):
    score: float


# =========================
# Step Result (Helper)
# =========================
class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict = Field(default_factory=dict)