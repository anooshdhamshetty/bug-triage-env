# =========================
# SIGNAL CONFIGURATION
# =========================

SIGNAL_CONFIG = {

    # 🔹 DOMAIN (Highest Priority)
    "domain": {
        "payment": {"category": "backend", "weight": 4},
        "checkout": {"category": "backend", "weight": 3},
        "login": {"category": "backend", "weight": 4},
        "auth": {"category": "backend", "weight": 4},
        "database": {"category": "database", "weight": 4},
        "sql": {"category": "database", "weight": 4},
        "query": {"category": "database", "weight": 3}
    },

    # 🔹 FAILURE
    "failure": {
        "crash": {"category": "backend", "weight": 3},
        "timeout": {"category": "backend", "weight": 3},
        "error": {"category": "backend", "weight": 1},
        "fail": {"category": "backend", "weight": 2},
        "not working": {"category": "backend", "weight": 2}
    },

    # 🔹 PERFORMANCE
    "performance": {
        "slow": {"category": "backend", "weight": 2},
        "lag": {"category": "backend", "weight": 2},
        "delay": {"category": "backend", "weight": 2}
    },

    # 🔹 INTERACTION (UI)
    "interaction": {
        "button": {"category": "ui", "weight": 2},
        "click": {"category": "ui", "weight": 2},
        "dropdown": {"category": "ui", "weight": 2},
        "form": {"category": "ui", "weight": 2}
    },

    # 🔹 VISUAL UI
    "ui_visual": {
        "alignment": {"category": "ui", "weight": 3},
        "layout": {"category": "ui", "weight": 3},
        "css": {"category": "ui", "weight": 3},
        "responsive": {"category": "ui", "weight": 3}
    },

    # 🔹 SYSTEM
    "system": {
        "api": {"category": "backend", "weight": 3},
        "server": {"category": "backend", "weight": 3},
        "service": {"category": "backend", "weight": 2},
        "endpoint": {"category": "backend", "weight": 3}
    },

    # 🔹 NETWORK
    "network": {
        "network": {"category": "network", "weight": 4},
        "latency": {"category": "network", "weight": 3},
        "connection": {"category": "network", "weight": 3},
        "dns": {"category": "network", "weight": 4}
    }
}


# =========================
# TEXT PREPROCESSING
# =========================

def preprocess_text(bug):
    """
    Combine all text fields into one string
    """
    text = " ".join([
        bug.get("title", ""),
        bug.get("description", ""),
        bug.get("logs", "")
    ])
    return text.lower()


# =========================
# SIGNAL EXTRACTION
# =========================

def extract_signals(bug):
    """
    Extract signals from bug text
    Returns list of matched signals
    """
    text = preprocess_text(bug)

    signals = []

    for group_name, keywords in SIGNAL_CONFIG.items():
        for keyword, info in keywords.items():
            if keyword in text:
                signals.append({
                    "type": group_name,
                    "keyword": keyword,
                    "category": info["category"],
                    "weight": info["weight"]
                })

    return signals