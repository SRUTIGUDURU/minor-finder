from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def parse_form_data(form_data):
    """
    Parses and structures the form data from the survey form submission.
    """
    # Get branch data
    selected_branch = form_data.get("branch", "")
    branch_like = form_data.get("branchLike", "")
    dual_branch = form_data.get("dualBranch", "")
    
    # Initialize branch scores
    branch_scores = {
        "CS": 0, "ECE": 0, "EEE": 0, "ENI": 0, "MECH": 0, 
        "CHEM": 0, "CIVIL": 0, "ECO": 0, "MATH": 0,
        "PHYSICS": 0, "CHEMISTRY": 0, "BIO": 0
    }
    
    # Set score for selected branch
    if selected_branch in branch_scores:
        branch_scores[selected_branch] = 7.5 if branch_like == "yes" else 2.5
    
    # Set score for dual branch - handle Physics specially
    if dual_branch in branch_scores and dual_branch != "None":
        if dual_branch == "PHYSICS":
            branch_scores["PHYSICS"] = 0  # Don't count PHYSICS if it's the dual branch
        else:
            branch_scores[dual_branch] = 7.5
    
    # Get ratings for other branches
    for branch in branch_scores.keys():
        if branch != selected_branch and branch != dual_branch:
            try:
                branch_scores[branch] = float(form_data.get(branch, 0))
            except (ValueError, TypeError):
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
    selected_languages = form_data.get("selectedLanguages", "").split(", ") if form_data.get("selectedLanguages") else []
    programming_languages_scores = {
        lang: 5 if lang in selected_languages else 0
        for lang in ["Matlab", "Simulink", "Python", "C++", "C", "R", "Java", "Go", "SQL", "JavaScript", "Julia"]
    }

    return branch_scores, opels_scores, programming_languages_scores

def aero(branch_scores, opels_scores, programming_languages_scores):
    aeronautics_score = opels_scores["Aeronautics"]
    if aeronautics_score == 0:
        return 0
    total_score = (
        aeronautics_score +
        branch_scores["EEE"] +
        branch_scores["MECH"] +
        programming_languages_scores["Matlab"] +
        programming_languages_scores["Simulink"] +
        programming_languages_scores["Python"] +
        programming_languages_scores["C++"]
    )
    return (total_score / 37.5) * 100

def ce(branch_scores, opels_scores, programming_languages_scores):
    total_score = (
        branch_scores["ECO"] +
        branch_scores["CS"] +
        branch_scores["MATH"] +
        programming_languages_scores["C"] +
        programming_languages_scores["C++"] +
        programming_languages_scores["Python"] +
        programming_languages_scores["R"] +
        programming_languages_scores["Java"] +
        programming_languages_scores["Go"] +
        programming_languages_scores["SQL"] +
        programming_languages_scores["JavaScript"] +
        programming_languages_scores["Julia"]
    )
    return (total_score / 62.5) * 100

def cni(branch_scores, opels_scores, programming_languages_scores):
    cs_score = branch_scores["CS"]
    if cs_score in [7.5, 2.5]:
        return 0
    total_score = (
        cs_score +
        programming_languages_scores["C"] +
        programming_languages_scores["C++"] +
        programming_languages_scores["Python"] +
        programming_languages_scores["R"] +
        programming_languages_scores["Java"] +
        programming_languages_scores["Go"] +
        programming_languages_scores["SQL"] +
        programming_languages_scores["JavaScript"] +
        programming_languages_scores["Julia"]
    )
    return (total_score / 50) * 100

def ds(branch_scores, opels_scores, programming_languages_scores):
    total_score = (
        branch_scores["MATH"] +
        branch_scores["CS"]
    )
    return (total_score / 35) * 100

def entrepreneur(branch_scores, opels_scores, programming_languages_scores):
    score = opels_scores["Entrepreneurship"]
    if score == 0:
        return 0
    total_score = score + branch_scores["ECO"]
    return (total_score / 12.5) * 100

def fin(branch_scores, opels_scores, programming_languages_scores):
    finance_score = opels_scores["Finance"]
    return (finance_score / 5) * 100 if finance_score != 0 else 0

def mse(branch_scores, opels_scores, programming_languages_scores):
    materials_score = opels_scores["MaterialSciences"]
    if materials_score == 0:
        return 0
    total_score = (
        materials_score +
        branch_scores["CHEM"] +
        branch_scores["MECH"] +
        branch_scores["CHEMISTRY"] +
        branch_scores["PHYSICS"]
    )
    return (total_score / 30) * 100

def phy(branch_scores, opels_scores, programming_languages_scores):
    physics_score = branch_scores["PHYSICS"]
    # If PHYSICS is 0 (meaning it's the dual branch), return 0
    if physics_score>0:
        return 0
    else:
        total_score = (
        physics_score +
        branch_scores["EEE"] +
        branch_scores["ENI"] +
        branch_scores["ECE"]
    )
    return (total_score / 22.5) * 100

def raa(branch_scores, opels_scores, programming_languages_scores):
    robotics_score = opels_scores["RoboticsAndAutomation"]
    if robotics_score == 0:
        return 0
    total_score = (
        robotics_score +
        branch_scores["ECE"] +
        branch_scores["EEE"] +
        branch_scores["ENI"] +
        branch_scores["MECH"]
    )
    return (total_score / 27.5) * 100

def sca(branch_scores, opels_scores, programming_languages_scores):
    total_score = (
        branch_scores["MATH"] +
        branch_scores["MECH"]
    )
    return (total_score / 15) * 100

def semiconductors(branch_scores, opels_scores, programming_languages_scores):
    total_score = (
        branch_scores["EEE"] +
        branch_scores["ECE"] +
        branch_scores["ENI"]
    )
    return (total_score / 35) * 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        form_data = request.form.to_dict()
        
        # Parse the form data
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
        
        return jsonify({
            "success": True,
            "top_5_minors": top_5_minors
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)

