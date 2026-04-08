from typing import Dict


# =========================
# COMPONENT WEIGHTS
# =========================

CATEGORY_WEIGHT = 0.3
SEVERITY_WEIGHT = 0.3
TEAM_WEIGHT = 0.4


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

    return round(score, 2)


# =========================
# TASK-SPECIFIC GRADERS
# =========================

def grade_easy(pred: Dict, expected: Dict) -> float:
    """
    Easy task → only category
    """

    if pred.get("category") == expected.get("category"):
        return 1.0

    return 0.0


def grade_medium(pred: Dict, expected: Dict) -> float:
    """
    Medium → category + severity
    """

    score = 0.0

    if pred.get("category") == expected.get("category"):
        score += 0.5

    if pred.get("severity") == expected.get("severity"):
        score += 0.5

    return round(score, 2)


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