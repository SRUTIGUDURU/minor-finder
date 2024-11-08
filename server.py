from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Form server is running."

@app.route('/submit', methods=['POST'])
def submit_form():
    # Retrieve form data
    data = request.form.to_dict()

    # Checkboxes for programming languages are handled differently
    programming_languages = request.form.getlist('programmingLanguages')

    # Assign '0' to any field that is empty
    processed_data = {key: value if value else "0" for key, value in data.items()}
    processed_data["programmingLanguages"] = programming_languages if programming_languages else ["0"]

    # Save to JSON file
    with open("user_data.json", "w") as file:
        json.dump(processed_data, file, indent=4)

    return jsonify({"status": "success", "data": processed_data})

if __name__ == "__main__":
    app.run(debug=True)
