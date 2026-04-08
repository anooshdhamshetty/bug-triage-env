BUGS = [

    # =========================
    # 🔹 BACKEND / PAYMENT
    # =========================
    {
        "input": {
            "title": "Payment failed during checkout",
            "description": "User charged but order not created",
            "logs": "timeout error in payment service",
            "user_impact": "high",
            "frequency": 120,
            "module_hint": "payment"
        },
        "expected": {
            "category": "backend",
            "severity": "high",
            "team": "payments_team"
        }
    },

    {
        "input": {
            "title": "Checkout API failing",
            "description": "Orders not getting processed",
            "logs": "500 server error",
            "user_impact": "high",
            "frequency": 80,
            "module_hint": "payment"
        },
        "expected": {
            "category": "backend",
            "severity": "high",
            "team": "payments_team"
        }
    },

    # =========================
    # 🔹 UI ISSUES
    # =========================
    {
        "input": {
            "title": "Button not clickable on homepage",
            "description": "Clicking submit button does nothing",
            "logs": "",
            "user_impact": "medium",
            "frequency": 25,
            "module_hint": "ui"
        },
        "expected": {
            "category": "ui",
            "severity": "medium",
            "team": "frontend_team"
        }
    },

    {
        "input": {
            "title": "Text alignment broken",
            "description": "UI looks misaligned on mobile screen",
            "logs": "",
            "user_impact": "low",
            "frequency": 10,
            "module_hint": "ui"
        },
        "expected": {
            "category": "ui",
            "severity": "low",
            "team": "frontend_team"
        }
    },

    # =========================
    # 🔹 DATABASE ISSUES
    # =========================
    {
        "input": {
            "title": "Database query too slow",
            "description": "Reports page taking long time to load",
            "logs": "slow SQL query detected",
            "user_impact": "medium",
            "frequency": 60,
            "module_hint": "database"
        },
        "expected": {
            "category": "database",
            "severity": "medium",
            "team": "backend_team"
        }
    },

    {
        "input": {
            "title": "Database connection failed",
            "description": "Unable to fetch user data",
            "logs": "connection refused error",
            "user_impact": "high",
            "frequency": 90,
            "module_hint": "database"
        },
        "expected": {
            "category": "database",
            "severity": "high",
            "team": "backend_team"
        }
    },

    # =========================
    # 🔹 NETWORK ISSUES
    # =========================
    {
        "input": {
            "title": "API request failing intermittently",
            "description": "Requests timeout randomly",
            "logs": "network timeout",
            "user_impact": "medium",
            "frequency": 50,
            "module_hint": "network"
        },
        "expected": {
            "category": "network",
            "severity": "medium",
            "team": "infra_team"
        }
    },

    {
        "input": {
            "title": "DNS resolution failure",
            "description": "Users unable to reach service",
            "logs": "DNS lookup failed",
            "user_impact": "high",
            "frequency": 70,
            "module_hint": "network"
        },
        "expected": {
            "category": "network",
            "severity": "high",
            "team": "infra_team"
        }
    },

    # =========================
    # 🔹 AUTH / LOGIN
    # =========================
    {
        "input": {
            "title": "Login not working",
            "description": "Users unable to login",
            "logs": "auth service error",
            "user_impact": "high",
            "frequency": 100,
            "module_hint": "auth"
        },
        "expected": {
            "category": "backend",
            "severity": "high",
            "team": "backend_team"
        }
    },

    # =========================
    # 🔹 PERFORMANCE
    # =========================
    {
        "input": {
            "title": "Application very slow",
            "description": "Pages take long to load",
            "logs": "",
            "user_impact": "medium",
            "frequency": 40,
            "module_hint": ""
        },
        "expected": {
            "category": "backend",
            "severity": "medium",
            "team": "backend_team"
        }
    },

    # =========================
    # 🔹 MIXED CASES (IMPORTANT)
    # =========================
    {
        "input": {
            "title": "Payment button crashes app",
            "description": "Clicking button causes failure",
            "logs": "payment service crash",
            "user_impact": "high",
            "frequency": 85,
            "module_hint": "payment"
        },
        "expected": {
            "category": "backend",
            "severity": "high",
            "team": "payments_team"
        }
    },

    {
        "input": {
            "title": "Dropdown not working",
            "description": "User cannot select options",
            "logs": "",
            "user_impact": "low",
            "frequency": 15,
            "module_hint": "ui"
        },
        "expected": {
            "category": "ui",
            "severity": "low",
            "team": "frontend_team"
        }
    },

    {
        "input": {
            "title": "Server error on API call",
            "description": "Backend returning 500 error",
            "logs": "internal server error",
            "user_impact": "high",
            "frequency": 75,
            "module_hint": "backend"
        },
        "expected": {
            "category": "backend",
            "severity": "high",
            "team": "backend_team"
        }
    },

    {
        "input": {
            "title": "Connection latency high",
            "description": "Slow response from server",
            "logs": "network latency detected",
            "user_impact": "medium",
            "frequency": 55,
            "module_hint": "network"
        },
        "expected": {
            "category": "network",
            "severity": "medium",
            "team": "infra_team"
        }
    }

]