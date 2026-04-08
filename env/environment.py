import random
from typing import Tuple, Dict, Any

from env.models import Observation, Action
from env.scorer import get_ground_truth
from data.bugs import BUGS


class BugTriageEnv:

    def __init__(self):
        self.bugs = BUGS
        self.current_bug = None
        self.current_step = 0
        self.done = False
        self.total_reward = 0.0

    # =========================
    # RESET
    # =========================
    def reset(self) -> Observation:
        """
        Start a new episode
        """
        self.current_bug = random.choice(self.bugs)
        self.current_step = 0
        self.done = False
        self.total_reward = 0.0

        return Observation(**self.current_bug["input"])

    # =========================
    # STATE
    # =========================
    def state(self) -> Observation:
        """
        Return current observation
        """
        return Observation(**self.current_bug["input"])

    # =========================
    # STEP
    # =========================
    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """
        Perform one step in environment
        """

        if self.done:
            raise Exception("Episode is done. Call reset().")

        correct = self.current_bug["expected"]

        reward = 0.0
        info = {}

        # -------------------------
        # STEP 0 → CATEGORY
        # -------------------------
        if self.current_step == 0:
            if action.category == correct["category"]:
                reward = 0.3
                info["category_correct"] = True
            else:
                reward = -0.2
                info["category_correct"] = False

        # -------------------------
        # STEP 1 → SEVERITY
        # -------------------------
        elif self.current_step == 1:
            if action.severity == correct["severity"]:
                reward = 0.3
                info["severity_correct"] = True
            else:
                reward = -0.2
                info["severity_correct"] = False

        # -------------------------
        # STEP 2 → TEAM
        # -------------------------
        elif self.current_step == 2:
            if action.team == correct["team"]:
                reward = 0.4
                info["team_correct"] = True
            else:
                reward = -0.2
                info["team_correct"] = False

        # accumulate reward
        self.total_reward += reward

        # move step forward
        self.current_step += 1

        # check if episode done
        if self.current_step >= 3:
            self.done = True

        return (
            Observation(**self.current_bug["input"]),
            reward,
            self.done,
            info
        )

    # =========================
    # FINAL SCORE
    # =========================
    def get_total_reward(self) -> float:
        """
        Return final episode score (0–1 clipped)
        """
        return max(0.0, min(1.0, self.total_reward))