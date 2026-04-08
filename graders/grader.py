from typing import Dict


# =========================
# COMPONENT WEIGHTS
# =========================

CATEGORY_WEIGHT = 0.3
SEVERITY_WEIGHT = 0.3
TEAM_WEIGHT = 0.4

SCORE_EPSILON = 0.01


# =========================
# CORE GRADING FUNCTION
# =========================

def grade_prediction(pred: Dict, expected: Dict) -> float:
    """
    Compare prediction with expected output
    Returns score in [0.0, 1.0]
    """

    score = 0.0

    # Category
    if pred.get("category") == expected.get("category"):
        score += CATEGORY_WEIGHT

    # Severity
    if pred.get("severity") == expected.get("severity"):
        score += SEVERITY_WEIGHT

    # Team
    if pred.get("team") == expected.get("team"):
        score += TEAM_WEIGHT

    score = round(score, 2)
    if score <= 0.0:
        return SCORE_EPSILON
    if score >= 1.0:
        return round(1.0 - SCORE_EPSILON, 2)
    return score


# =========================
# TASK-SPECIFIC GRADERS
# =========================

def grade_easy(pred: Dict, expected: Dict) -> float:
    """
    Easy task → only category
    """

    if pred.get("category") == expected.get("category"):
        return round(1.0 - SCORE_EPSILON, 2)

    return SCORE_EPSILON


def grade_medium(pred: Dict, expected: Dict) -> float:
    """
    Medium → category + severity
    """

    score = 0.0

    if pred.get("category") == expected.get("category"):
        score += 0.5

    if pred.get("severity") == expected.get("severity"):
        score += 0.5

    score = round(score, 2)
    if score <= 0.0:
        return SCORE_EPSILON
    if score >= 1.0:
        return round(1.0 - SCORE_EPSILON, 2)
    return score


def grade_hard(pred: Dict, expected: Dict) -> float:
    """
    Hard → full triage
    """

    return grade_prediction(pred, expected)


# =========================
# DISPATCHER
# =========================

def evaluate(task: str, pred: Dict, expected: Dict) -> float:
    """
    Route to correct grader
    """

    if task == "easy":
        return grade_easy(pred, expected)

    elif task == "medium":
        return grade_medium(pred, expected)

    elif task == "hard":
        return grade_hard(pred, expected)

    else:
        raise ValueError(f"Unknown task: {task}")