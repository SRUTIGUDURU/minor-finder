from flask import Flask, request, jsonify

app = Flask(__name__)

def parse_form_data(form_data):
    """
    Parses and structures the form data from the survey form submission.
    """
    branch_data = {
        "branch": form_data.get("branch", ""),
        "branch_like": form_data.get("branchLike", ""),
        "dual_branch": form_data.get("dualBranch", "")
    }

    branch_interest_ratings = {
        branch: int(form_data.get(branch, 0))
        for branch in ["CS", "ECE", "EEE", "ENI", "MECH", "CHEM", "CIVIL", "ECO", "MATH", "PHYSICS", "CHEMISTRY", "BIO"]
    }

    opels_scores = {
        "Aeronautics": int(form_data.get("Aeronautics", 0)),
        "Entrepreneurship": int(form_data.get("Entrepreneurship", 0)),
        "Finance": int(form_data.get("Finance", 0)),
        "MaterialSciences": int(form_data.get("MaterialSciences", 0)),
        "RoboticsAndAutomation": int(form_data.get("RoboticsAndAutomation", 0))
    }

    selected_languages = form_data.get("selectedLanguages", "").split(", ")
    programming_languages_scores = {
        lang: 5 if lang in selected_languages else 0
        for lang in ["Matlab", "Simulink", "Python", "C++", "C", "R", "Java", "Go", "SQL", "JavaScript", "Julia"]
    }

    return branch_data, branch_interest_ratings, opels_scores, programming_languages_scores

def aero(branch_data, opels_scores, programming_languages_scores):
    aeronautics_score = opels_scores["Aeronautics"]
    if aeronautics_score == 0:
        return 0
    total_score = (
        aeronautics_score +
        branch_data.get("EEE", 0) +
        branch_data.get("MECH", 0) +
        programming_languages_scores["Matlab"] +
        programming_languages_scores["Simulink"] +
        programming_languages_scores["Python"] +
        programming_languages_scores["C++"]
    )
    return total_score / 37.5

def ce(branch_data, opels_scores, programming_languages_scores):
    total_score = (
        branch_data.get("ECO", 0) +
        branch_data.get("CS", 0) +
        branch_data.get("MATH", 0) +
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
    return total_score / 62.5

def cni(branch_data, opels_scores, programming_languages_scores):
    cs_score = branch_data.get("CS", 0)
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
    return total_score / 50

def ds(branch_data, opels_scores, programming_languages_scores):
    total_score = (
        branch_data.get("MATH", 0) +
        branch_data.get("CS", 0)
    )
    return total_score / 35

def entrepreneur(branch_data, opels_scores, programming_languages_scores):
    score = opels_scores.get("Entrepreneurship", 0)
    if score == 0:
        return 0
    total_score = score + branch_data.get("ECO", 0)
    return total_score / 12.5

def fin(branch_data, opels_scores, programming_languages_scores):
    finance_score = opels_scores.get("Finance", 0)
    return finance_score / 5 if finance_score != 0 else 0

def management(branch_data, opels_scores, programming_languages_scores):
    management_score = opels_scores.get("Management", 0)
    if management_score == 0:
        return 0
    total_score = (
        management_score +
        branch_data.get("ECO", 0) +
        branch_data.get("MECH", 0)
    )
    return total_score / 20

def mse(branch_data, opels_scores, programming_languages_scores):
    materials_score = opels_scores.get("MaterialSciences", 0)
    if materials_score == 0:
        return 0
    total_score = (
        materials_score +
        branch_data.get("CHEM", 0) +
        branch_data.get("MECH", 0) +
        branch_data.get("CHEMISTRY", 0) +
        branch_data.get("PHYSICS", 0)
    )
    return total_score / 30

def phy(branch_data, opels_scores, programming_languages_scores):
    physics_score = branch_data.get("PHYSICS", 0)
    if physics_score == 7.5:
        return 0
    total_score = (
        physics_score +
        branch_data.get("EEE", 0) +
        branch_data.get("ENI", 0) +
        branch_data.get("ECE", 0)
    )
    return total_score / 22.5

def raa(branch_data, opels_scores, programming_languages_scores):
    robotics_score = opels_scores.get("RoboticsAndAutomation", 0)
    if robotics_score == 0:
        return 0
    total_score = (
        robotics_score +
        branch_data.get("ECE", 0) +
        branch_data.get("EEE", 0) +
        branch_data.get("ENI", 0) +
        branch_data.get("MECH", 0)
    )
    return total_score / 27.5

def sca(branch_data, opels_scores, programming_languages_scores):
    total_score = (
        branch_data.get("MATH", 0) +
        branch_data.get("MECH", 0)
    )
    return total_score / 15

def semiconductors(branch_data, opels_scores, programming_languages_scores):
    total_score = (
        branch_data.get("EEE", 0) +
        branch_data.get("ECE", 0) +
        branch_data.get("ENI", 0)
    )
    return total_score / 35

@app.route('/submit', methods=['POST'])
def submit_form():
    form_data = request.form.to_dict()
    form_data["selectedLanguages"] = request.form.get("selectedLanguages", "")

    branch_data, branch_interest_ratings, opels_scores, programming_languages_scores = parse_form_data(form_data)

    results = {
        "Aeronautics": aero(branch_data, opels_scores, programming_languages_scores),
        "Computing and Intelligence": cni(branch_data, opels_scores, programming_languages_scores),
        "Data Science": ds(branch_data, opels_scores, programming_languages_scores),
        "Entrepreneur": entrepreneur(branch_data, opels_scores, programming_languages_scores),
        "Finance": fin(branch_data, opels_scores, programming_languages_scores),
        "Computational Economics": ce(branch_data, opels_scores, programming_languages_scores),
        "Semiconductors": semiconductors(branch_data, opels_scores, programming_languages_scores),
        "Supply Chain Analysis": sca(branch_data, opels_scores, programming_languages_scores),
        "Robotics And Automation": raa(branch_data, opels_scores, programming_languages_scores),
        "Physics": phy(branch_data, opels_scores, programming_languages_scores),
        "Material Science Engineering": mse(branch_data, opels_scores, programming_languages_scores),
        "Management": management(branch_data, opels_scores, programming_languages_scores),
    }

    sorted_minors = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_minors = {name: score for name, score in sorted_minors}

    return jsonify(top_5_minors=top_5_minors)

if __name__ == '__main__':
    app.run(debug=True)


