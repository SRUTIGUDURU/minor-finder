from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

class MinorScoreCalculator:
    @staticmethod
    def calculate_percentage(score, max_score):
        return (score / max_score) * 100 if max_score > 0 else 0

    def __init__(self, branch_scores, opels_scores, programming_languages_scores):
        self.branch_scores = branch_scores
        self.opels_scores = opels_scores
        self.programming_languages_scores = programming_languages_scores

    def aero(self):
        if self.opels_scores["Aeronautics"] == 0:
            return 0
        total_score = sum([
            self.opels_scores["Aeronautics"],
            self.branch_scores["EEE"],
            self.branch_scores["MECHANICAL"],
            self.programming_languages_scores["Matlab"],
            self.programming_languages_scores["Simulink"],
            self.programming_languages_scores["Python"],
            self.programming_languages_scores["C++"]
        ])
        return self.calculate_percentage(total_score, 37.5)

    def ce(self):
        programming_score = sum(
            self.programming_languages_scores[lang]
            for lang in ["C", "C++", "Python", "R", "Java", "Go", "SQL", "JavaScript", "Julia"]
        )
        total_score = sum([
            self.branch_scores["ECONOMICS"],
            self.branch_scores["CSE"],
            self.branch_scores["MATHEMATICS"],
            programming_score
        ])
        return self.calculate_percentage(total_score, 62.5)

    def cni(self):
        cs_score = self.branch_scores["CSE"]
        if cs_score in [7.5, 2.5]:
            return 0
        programming_score = sum(
            self.programming_languages_scores[lang]
            for lang in ["C", "C++", "Python", "R", "Java", "Go", "SQL", "JavaScript", "Julia"]
        )
        return self.calculate_percentage(cs_score + programming_score, 50)

    def ds(self):
        total_score = self.branch_scores["MATHEMATICS"] + self.branch_scores["CSE"]
        return self.calculate_percentage(total_score, 35)

    def entrepreneur(self):
        score = self.opels_scores["Entrepreneurship"]
        if score == 0:
            return 0
        return self.calculate_percentage(score + self.branch_scores["ECONOMICS"], 12.5)

    def fin(self):
        return self.calculate_percentage(self.opels_scores["Finance"], 5)

    def mse(self):
        materials_score = self.opels_scores["MaterialSciences"]
        if materials_score == 0:
            return 0
        total_score = sum([
            materials_score,
            self.branch_scores["CHEMICAL"],
            self.branch_scores["MECHANICAL"],
            self.branch_scores["CHEMISTRY"],
            self.branch_scores["PHYSICS"]
        ])
        return self.calculate_percentage(total_score, 30)

    def phy(self):
        physics_score = self.branch_scores["PHYSICS"]
        if physics_score in [7.5, 0]:
            return 0
        total_score = sum([
            physics_score,
            self.branch_scores["EEE"],
            self.branch_scores["ENI"],
            self.branch_scores["ECE"]
        ])
        return self.calculate_percentage(total_score, 22.5)

    def raa(self):
        robotics_score = self.opels_scores["RoboticsAndAutomation"]
        if robotics_score == 0:
            return 0
        total_score = sum([
            robotics_score,
            self.branch_scores["ECE"],
            self.branch_scores["EEE"],
            self.branch_scores["ENI"],
            self.branch_scores["MECHANICAL"]
        ])
        return self.calculate_percentage(total_score, 27.5)

    def sca(self):
        total_score = self.branch_scores["MATHEMATICS"] + self.branch_scores["MECHANICAL"]
        return self.calculate_percentage(total_score, 15)

    def semiconductors(self):
        total_score = sum([
            self.branch_scores["EEE"],
            self.branch_scores["ECE"],
            self.branch_scores["ENI"]
        ])
        return self.calculate_percentage(total_score, 35)

class FormDataParser:
    @staticmethod
    def parse_form_data(form_data):
        # Parse branch data
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

        # Get branch ratings
        for branch in branch_scores:
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

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Parse form data
        form_data = request.form.to_dict()
        branch_scores, opels_scores, programming_languages_scores = FormDataParser.parse_form_data(form_data)
        
        # Calculate minor scores
        calculator = MinorScoreCalculator(branch_scores, opels_scores, programming_languages_scores)
        
        results = {
            "Aeronautics": calculator.aero(),
            "Computing and Intelligence": calculator.cni(),
            "Data Science": calculator.ds(),
            "Entrepreneurship": calculator.entrepreneur(),
            "Finance": calculator.fin(),
            "Computational Economics": calculator.ce(),
            "Semiconductors": calculator.semiconductors(),
            "Supply Chain Analysis": calculator.sca(),
            "Robotics And Automation": calculator.raa(),
            "Physics": calculator.phy(),
            "Material Science Engineering": calculator.mse()
        }
        
        # Sort and get top 5 minors
        sorted_minors = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_minors = {name: round(score, 2) for name, score in sorted_minors}
        
        return jsonify({"success": True, "top_5_minors": top_5_minors})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
