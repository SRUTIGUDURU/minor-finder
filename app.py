from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def parse_form_data(form_data):
    """
    Parses form data and structures it into three categories:
    branch scores, OPEL scores, and programming language scores.
    """
    # Branch data
    selected_branch = form_data.get("branch", "")
    branch_like = form_data.get("branchLike", "").lower() == "yes"
    dual_branch = form_data.get("dualBranch", "")
    
    # Initialize branch scores
    branch_scores = {
        "CSE": 0, "ECE": 0, "EEE": 0, "ENI": 0, "MECHANICAL": 0,
        "CHEMICAL": 0, "CIVIL": 0, "ECONOMICS": 0, "MATHEMATICS": 0,
        "PHYSICS": 0, "CHEMISTRY": 0, "BIOLOGY": 0
    }
    
    # Set score based on branch preference
    if selected_branch in branch_scores:
        branch_scores[selected_branch] = 7.5 if branch_like else 2.5

    # Get branch ratings, excluding selected and dual branches
    for branch, score in branch_scores.items():
        if branch != selected_branch and branch != dual_branch:
            try:
                branch_scores[branch] = float(form_data.get(branch, 0))
            except ValueError:
                branch_scores[branch] = 0

    # Parse OPEL scores
    opels_scores = {
        "Aeronautics": float(form_data.get("Aeronautics", 0)),
        "Entrepreneurship": float(form_data.get("Entrepreneurship", 0)),
        "Finance": float(form_data.get("Finance", 0)),
        "MaterialSciences": float(form_data.get("MaterialSciences", 0)),
        "RoboticsAndAutomation": float(form_data.get("RoboticsAndAutomation", 0))
    }

    # Parse programming languages
    selected_languages = form_data.get("selectedLanguages", "").split(", ")
    programming_languages_scores = {
        lang: 5 if lang in selected_languages else 0
        for lang in ["Matlab", "Simulink", "Python", "C++", "C", "R", "Java", "Go", "SQL", "JavaScript", "Julia"]
    }

    return branch_scores, opels_scores, programming_languages_scores

# Minor score calculation helpers
def calculate_percentage(score, max_score):
    return (score / max_score) * 100 if max_score > 0 else 0

# Individual minor scoring functions
def aero(branch_scores, opels_scores, programming_languages_scores):
    if opels_scores["Aeronautics"] == 0:
        return 0
    total_score = (
        opels_scores["Aeronautics"] +
        branch_scores["EEE"] +
        branch_scores["MECHANICAL"] +
        programming_languages_scores["Matlab"] +
        programming_languages_scores["Simulink"] +
        programming_languages_scores["Python"] +
        programming_languages_scores["C++"]
    )
    return calculate_percentage(total_score, 37.5)

def ce(branch_scores, opels_scores, programming_languages_scores):
    total_score = (
        branch_scores["ECONOMICS"] +
        branch_scores["CSE"] +
        branch_scores["MATHEMATICS"] +
        sum(programming_languages_scores[lang] for lang in ["C", "C++", "Python", "R", "Java", "Go", "SQL", "JavaScript", "Julia"])
    )
    return calculate_percentage(total_score, 62.5)

def cni(branch_scores, opels_scores, programming_languages_scores):
    cs_score = branch_scores["CSE"]
    if cs_score in [7.5, 2.5]:
        return 0
    total_score = (
        cs_score +
        sum(programming_languages_scores[lang] for lang in ["C", "C++", "Python", "R", "Java", "Go", "SQL", "JavaScript", "Julia"])
    )
    return calculate_percentage(total_score, 50)

def ds(branch_scores, opels_scores, programming_languages_scores):
    total_score = branch_scores["MATHEMATICS"] + branch_scores["CSE"]
    return calculate_percentage(total_score, 35)

def entrepreneur(branch_scores, opels_scores, programming_languages_scores):
    score = opels_scores["Entrepreneurship"]
    if score == 0:
        return 0
    return calculate_percentage(score + branch_scores["ECONOMICS"], 12.5)

def fin(branch_scores, opels_scores, programming_languages_scores):
    return calculate_percentage(opels_scores["Finance"], 5)

def mse(branch_scores, opels_scores, programming_languages_scores):
    materials_score = opels_scores["MaterialSciences"]
    if materials_score == 0:
        return 0
    total_score = (
        materials_score +
        branch_scores["CHEMICAL"] +
        branch_scores["MECHANICAL"] +
        branch_scores["CHEMISTRY"] +
        branch_scores["PHYSICS"]
    )
    return calculate_percentage(total_score, 30)

def phy(branch_scores, opels_scores, programming_languages_scores):
    physics_score = branch_scores["PHYSICS"]
    if physics_score in [7.5, 0]:  # 7.5 or 0 indicates it's the dual branch or not liked
        return 0
    total_score = (
        physics_score +
        branch_scores["EEE"] +
        branch_scores["ENI"] +
        branch_scores["ECE"]
    )
    return calculate_percentage(total_score, 22.5)

def raa(branch_scores, opels_scores, programming_languages_scores):
    robotics_score = opels_scores["RoboticsAndAutomation"]
    if robotics_score == 0:
        return 0
    total_score = (
        robotics_score +
        branch_scores["ECE"] +
        branch_scores["EEE"] +
        branch_scores["ENI"] +
        branch_scores["MECHANICAL"]
    )
    return calculate_percentage(total_score, 27.5)

def sca(branch_scores, opels_scores, programming_languages_scores):
    total_score = branch_scores["MATHEMATICS"] + branch_scores["MECHANICAL"]
    return calculate_percentage(total_score, 15)

def semiconductors(branch_scores, opels_scores, programming_languages_scores):
    total_score = branch_scores["EEE"] + branch_scores["ECE"] + branch_scores["ENI"]
    return calculate_percentage(total_score, 35)

# Route handlers
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        form_data = request.form.to_dict()
        branch_scores, opels_scores, programming_languages_scores = parse_form_data(form_data)
        
        # Calculate scores for each minor
        results = {
            "Aeronautics": aero(branch_scores, opels_scores, programming_languages_scores),
            "Computing and Intelligence": cni(branch_scores, opels_scores, programming_languages_scores),
            "Data Science": ds(branch_scores, opels_scores, programming_languages_scores),
            "Entrepreneurship": entrepreneur(branch_scores, opels_scores, programming_languages_scores),
            "Finance": fin(branch_scores, opels_scores, programming_languages_scores),
            "Computational Economics": ce(branch_scores, opels_scores, programming_languages_scores),
            "Semiconductors": semiconductors(branch_scores, opels_scores, programming_languages_scores),
            "Supply Chain Analysis": sca(branch_scores, opels_scores, programming_languages_scores),
            "Robotics And Automation": raa(branch_scores, opels_scores, programming_languages_scores),
            "Physics": phy(branch_scores, opels_scores, programming_languages_scores),
            "Material Science Engineering": mse(branch_scores, opels_scores, programming_languages_scores)
        }
        
        # Sort and get top 5 minors
        sorted_minors = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_minors = {name: round(score, 2) for name, score in sorted_minors}
        
        return jsonify({"success": True, "top_5_minors": top_5_minors})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
