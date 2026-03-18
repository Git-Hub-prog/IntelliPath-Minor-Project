import os
from flask import Flask
from routes import register_routes

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# --- Backend Scoring Logic & Weights ---
# Each option maps to careers it supports with associated weights
CAREER_WEIGHTS = {
    # Step 1: Learning & Interest Style
    "q1": {
        "frontend-uiux": {"frontend": 10, "uiux": 10, "mobile": 5, "fullstack": 3},
        "backend-logic": {"backend": 10, "devops": 8, "datascience": 8, "cybersecurity": 8, "swe": 5}
    },
    "q2": {
        "exploration": {"ml": 5, "datascience": 8, "blockchain": 8, "ai": 8},
        "guided": {"testing": 5, "swe": 3},
        "visual-learner": {"frontend": 8, "uiux": 8, "gamedev": 5}
    },
    "q3": {
        "examples": {"frontend": 5, "uiux": 5, "mobile": 5},
        "rules-steps": {"backend": 5, "devops": 10, "testing": 10, "cybersecurity": 8},
        "hands-on": {"swe": 8, "fullstack": 8, "gamedev": 8, "blockchain": 5}
    },
    "q4": {
        "data-math": {"datascience": 12, "ml": 12, "dataanalyst": 12, "gamedev": 5},
        "neutral-math": {"swe": 5, "backend": 5, "fullstack": 5},
        "design-focused": {"frontend": 10, "uiux": 12}
    },
    # Step 2: Problem Solving & Thinking
    "q5": {
        "persistence": {"blockchain": 8, "cybersecurity": 10, "backend": 5},
        "resourceful": {"fullstack": 8, "swe": 8, "devops": 5},
        "patience": {"testing": 8, "ml": 8}
    },
    "q6": {
        "fast-results": {"frontend": 10, "uiux": 5, "mobile": 8},
        "deep-logic": {"backend": 10, "datascience": 8, "ml": 8, "blockchain": 10, "cybersecurity": 8}
    },
    "q7": {
        "calm": {"devops": 10, "cybersecurity": 10, "backend": 5},
        "nervous": {"uiux": 5, "dataanalyst": 5, "testing": 5},
        "driven": {"fullstack": 8, "swe": 8, "gamedev": 10, "ai": 8}
    },
    "q8": {
        "uiux-front": {"frontend": 12, "uiux": 12, "mobile": 5},
        "backend-data": {"backend": 10, "datascience": 10, "ml": 10, "dataanalyst": 10},
        "devops-sys": {"devops": 12, "cybersecurity": 12, "blockchain": 5}
    },
    # Step 3: Work Style & Personality
    "q9": {
        "routine": {"testing": 10, "dataanalyst": 8, "devops": 5},
        "variety": {"fullstack": 10, "swe": 8, "mobile": 8, "gamedev": 8},
        "optimization": {"backend": 10, "devops": 10, "ml": 8}
    },
    "q10": {
        "security-high": {"cybersecurity": 15, "blockchain": 8, "devops": 5},
        "security-med": {"backend": 5, "swe": 5},
        "security-low": {"uiux": 5, "frontend": 5}
    },
    "q11": {
        "structured": {"testing": 12, "dataanalyst": 10, "devops": 8},
        "creative": {"uiux": 12, "gamedev": 10, "frontend": 8, "ai": 8}
    },
    "q12": {
        "pm-ba": {"dataanalyst": 5, "swe": 3},
        "technical": {"backend": 10, "ml": 10, "blockchain": 10, "cybersecurity": 10},
        "creative-ui": {"uiux": 12, "frontend": 8, "mobile": 5}
    }
}

CAREER_NAMES = {
    "frontend": "Frontend Web Development",
    "backend": "Backend Systems Engineering",
    "fullstack": "Full-Stack Development",
    "mobile": "Mobile App Development",
    "datascience": "Data Science",
    "ml": "Machine Learning Engineering",
    "cybersecurity": "Cybersecurity Analyst",
    "devops": "DevOps & Cloud Engineering",
    "uiux": "UI/UX Designer",
    "gamedev": "Game Development",
    "testing": "Software Testing & QA",
    "blockchain": "Blockchain Engineering",
    "swe": "Software Engineer",
    "dataanalyst": "Data Analyst",
    "ai": "AI Engineer"
}

def calculate_scores(answers):
    """
    Calculate career scores based on submitted answers.
    """
    scores = {career: 0 for career in CAREER_NAMES.keys()}
    
    for q_id, selected_value in answers.items():
        if q_id in CAREER_WEIGHTS and selected_value in CAREER_WEIGHTS[q_id]:
            weights = CAREER_WEIGHTS[q_id][selected_value]
            for career, weight in weights.items():
                if career in scores:
                    scores[career] += weight
                    
    # Sort careers by score descending
    sorted_careers = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Map back to full names
    top_career_id = sorted_careers[0][0]
    top_matches_ids = [item[0] for item in sorted_careers[:3]]
    
    readable_results = {
        "top_career": CAREER_NAMES[top_career_id],
        "top_matches": [CAREER_NAMES[cid] for cid in top_matches_ids],
        "scores": {CAREER_NAMES[cid]: score for cid, score in scores.items() if score > 0}
    }
    
    return readable_results

# Attach scoring logic to app object for access in routes
app.calculate_scores = calculate_scores

# Register routes
register_routes(app)

if __name__ == '__main__':
    # Flask settings
    app.run(debug=True, port=5000)
