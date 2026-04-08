from collections import defaultdict
from env.signals import extract_signals


# =========================
# CATEGORIES
# =========================

CATEGORIES = ["ui", "backend", "database", "network"]


# =========================
# METADATA BOOST
# =========================

def apply_metadata_boost(scores, bug):
    """
    Adjust scores based on metadata
    """

    # module hint
    module = bug.get("module_hint", "").lower()
    if module == "payment":
        scores["backend"] += 2
    elif module == "ui":
        scores["ui"] += 2
    elif module == "database":
        scores["database"] += 2
    elif module == "network":
        scores["network"] += 2

    # user impact
    if bug.get("user_impact") == "high":
        scores["backend"] += 1

    # frequency
    if bug.get("frequency", 0) > 100:
        scores["backend"] += 1

    return scores


# =========================
# CATEGORY SCORING
# =========================

def score_categories(bug):
    """
    Compute score for each category
    """

    signals = extract_signals(bug)

    scores = defaultdict(int)

    # accumulate weights
    for signal in signals:
        category = signal["category"]
        weight = signal["weight"]
        scores[category] += weight

    # ensure all categories exist
    for cat in CATEGORIES:
        scores[cat] += 0

    # apply metadata
    scores = apply_metadata_boost(scores, bug)

    return scores, signals


# =========================
# FINAL CATEGORY DECISION
# =========================

def predict_category(bug):
    """
    Predict final category using weighted scoring
    """

    scores, signals = score_categories(bug)

    # get best category
    best_category = max(scores, key=scores.get)

    # compute confidence
    total_score = sum(scores.values())
    max_score = scores[best_category]

    if total_score == 0:
        confidence = 0.5
        best_category = "backend"  # default fallback
    else:
        confidence = max_score / total_score

    return {
        "category": best_category,
        "confidence": round(confidence, 2),
        "scores": dict(scores),
        "signals": signals
    }


# =========================
# SEVERITY LOGIC
# =========================

def predict_severity(bug):
    """
    Determine severity
    """

    if bug.get("user_impact") == "high":
        return "high"

    if bug.get("frequency", 0) > 80:
        return "high"

    if bug.get("frequency", 0) > 30:
        return "medium"

    return "low"


# =========================
# TEAM ASSIGNMENT
# =========================

def assign_team(category, bug):
    """
    Assign team based on category + domain
    """

    module = bug.get("module_hint", "").lower()

    if category == "ui":
        return "frontend_team"

    if category == "backend":
        if module == "payment":
            return "payments_team"
        return "backend_team"

    if category == "database":
        return "backend_team"

    if category == "network":
        return "infra_team"

    return "backend_team"


# =========================
# FULL DECISION PIPELINE
# =========================

def get_ground_truth(bug):
    """
    Full triage decision
    """

    category_result = predict_category(bug)
    category = category_result["category"]

    severity = predict_severity(bug)

    team = assign_team(category, bug)

    return {
        "category": category,
        "severity": severity,
        "team": team,
        "confidence": category_result["confidence"]
    }