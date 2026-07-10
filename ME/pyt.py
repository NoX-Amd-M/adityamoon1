from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple rule-based career suggestion data
CAREER_DB = {
    "frontend": {
        "career": "Frontend Developer",
        "why": "Your interest in design, UI, and web technologies along with your skill set aligns well with building user-facing web applications.",
        "roadmap": [
            "Learn HTML, CSS, and JavaScript fundamentals",
            "Master a frontend framework (React, Vue, or Angular)",
            "Understand responsive design and accessibility",
            "Learn version control (Git/GitHub)",
            "Build 3-5 portfolio projects",
            "Learn state management (Redux/Context API)",
            "Apply for internships or junior roles"
        ],
        "skills": ["HTML", "CSS", "JavaScript", "React", "Git", "Responsive Design", "REST APIs"],
        "resources": [
            "freeCodeCamp - Responsive Web Design",
            "The Odin Project - Frontend Path",
            "React Official Documentation",
            "MDN Web Docs"
        ]
    },
    "backend": {
        "career": "Backend Developer",
        "why": "Your analytical skills and interest in logic, databases, and server-side systems make backend development a strong fit.",
        "roadmap": [
            "Learn a backend language (Python, Java, or Node.js)",
            "Understand databases (SQL and NoSQL)",
            "Learn REST API design and development",
            "Study authentication and security basics",
            "Learn about caching, queues, and scalability",
            "Build and deploy backend projects",
            "Apply for backend/junior developer roles"
        ],
        "skills": ["Python/Node.js", "SQL", "API Design", "Git", "Docker", "System Design Basics"],
        "resources": [
            "Flask/Django Official Docs",
            "freeCodeCamp - Backend Development",
            "Designing Data-Intensive Applications (book)",
            "Postman Learning Center"
        ]
    },
    "data": {
        "career": "Data Analyst / Data Scientist",
        "why": "Your interest in numbers, patterns, and problem-solving suits a career in data analysis or data science.",
        "roadmap": [
            "Learn Python and libraries (Pandas, NumPy)",
            "Master SQL for data querying",
            "Learn data visualization (Matplotlib, Power BI, Tableau)",
            "Study statistics and probability",
            "Learn machine learning basics (Scikit-learn)",
            "Work on real-world datasets/projects",
            "Apply for data analyst/junior data scientist roles"
        ],
        "skills": ["Python", "SQL", "Pandas", "Statistics", "Data Visualization", "Machine Learning Basics"],
        "resources": [
            "Kaggle Learn",
            "freeCodeCamp - Data Analysis with Python",
            "StatQuest YouTube Channel",
            "Google Data Analytics Certificate"
        ]
    },
    "design": {
        "career": "UI/UX Designer",
        "why": "Your creativity and interest in user experience and visual design make UI/UX design a great path.",
        "roadmap": [
            "Learn design fundamentals (color, typography, layout)",
            "Master design tools (Figma, Adobe XD)",
            "Study UX research and usability principles",
            "Build wireframes and prototypes",
            "Create a design portfolio with case studies",
            "Get feedback through design communities",
            "Apply for junior UI/UX roles or freelance"
        ],
        "skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Typography", "Design Systems"],
        "resources": [
            "Google UX Design Certificate",
            "Figma Official Tutorials",
            "Laws of UX (website)",
            "Dribbble & Behance for inspiration"
        ]
    },
    "default": {
        "career": "Software Developer",
        "why": "Based on your profile, a general software development path offers flexibility to explore multiple domains.",
        "roadmap": [
            "Learn a programming language (Python/Java/JavaScript)",
            "Understand data structures and algorithms",
            "Learn Git and version control",
            "Build small to medium projects",
            "Learn basics of web/app development",
            "Contribute to open source",
            "Apply for entry-level developer roles"
        ],
        "skills": ["Programming Fundamentals", "DSA", "Git", "Problem Solving", "Basic Web Development"],
        "resources": [
            "freeCodeCamp",
            "CS50 by Harvard (edX)",
            "LeetCode for practice",
            "GitHub Learning Lab"
        ]
    }
}


def determine_career(interests: str, skills: str, goal: str) -> dict:
    """
    Simple keyword-matching logic to pick a career path.
    Replace this with an AI/ML model or LLM call for smarter suggestions.
    """
    combined_text = f"{interests} {skills} {goal}".lower()

    if any(word in combined_text for word in ["ui", "ux", "design", "figma", "graphic"]):
        return CAREER_DB["design"]
    elif any(word in combined_text for word in ["data", "analysis", "machine learning", "ml", "statistics", "sql"]):
        return CAREER_DB["data"]
    elif any(word in combined_text for word in ["backend", "server", "api", "database", "node", "django", "flask"]):
        return CAREER_DB["backend"]
    elif any(word in combined_text for word in ["frontend", "react", "html", "css", "javascript", "web design"]):
        return CAREER_DB["frontend"]
    else:
        return CAREER_DB["default"]


@app.route("/generate", methods=["POST"])
def generate_roadmap():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    name = data.get("name", "").strip()
    education = data.get("education", "").strip()
    interests = data.get("interests", "").strip()
    skills = data.get("skills", "").strip()
    goal = data.get("goal", "").strip()

    # Basic validation
    if not interests and not skills and not goal:
        return jsonify({
            "error": "At least one of 'interests', 'skills', or 'goal' must be provided"
        }), 400

    career_info = determine_career(interests, skills, goal)

    response = {
        "name": name,
        "education": education,
        "career": career_info["career"],
        "why": career_info["why"],
        "roadmap": career_info["roadmap"],
        "skills": career_info["skills"],
        "resources": career_info["resources"]
    }

    return jsonify(response), 200


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Career Roadmap Generator API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)