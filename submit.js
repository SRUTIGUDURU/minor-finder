class MinorFinder {
    constructor() {
        this.branchSelect = document.getElementById('branch');
        this.dualBranchSelect = document.getElementById('dualBranch');
        this.branchRatingsContainer = document.querySelector('.branch-ratings-container');
        this.financeDiv = document.getElementById('financeDiv');
        this.form = document.getElementById('surveyForm');
        this.results = document.getElementById('results');
        this.topMinorsList = document.getElementById('topMinors');

        this.allBranches = {
            "CSE": "Computer Science and Engineering",
            "ECE": "Electronics and Communication Engineering",
            "EEE": "Electrical and Electronics Engineering",
            "ENI": "Electronics and Instrumentation",
            "MECHANICAL": "Mechanical Engineering",
            "CHEMICAL": "Chemical Engineering",
            "CIVIL": "Civil Engineering",
            "ECONOMICS": "Economics",
            "MATHEMATICS": "Mathematics",
            "PHYSICS": "Physics",
            "CHEMISTRY": "Chemistry",
            "BIOLOGY": "Biology"
        };

        this.initializeEventListeners();
        this.updateBranchRatings(); // Initial rendering of branch ratings
    }

    initializeEventListeners() {
        this.branchSelect.addEventListener('change', () => this.updateBranchRatings());
        this.dualBranchSelect.addEventListener('change', () => this.updateBranchRatings());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    updateBranchRatings() {
        const selectedBranch = this.branchSelect.value;
        const selectedDualBranch = this.dualBranchSelect.value;

        // Clear current branch ratings
        this.branchRatingsContainer.innerHTML = '';

        const excludedBranches = new Set(["MnC", "PHARMACY", selectedBranch, selectedDualBranch]);

        if (selectedBranch === "MnC") {
            excludedBranches.add("CSE");
            excludedBranches.add("MATHEMATICS");
        }

        Object.entries(this.allBranches)
            .filter(([code]) => !excludedBranches.has(code))
            .forEach(([code, name]) => {
                const ratingGroup = this.createRatingGroup(code, name);
                this.branchRatingsContainer.appendChild(ratingGroup);
            });

        this.financeDiv.style.display = selectedDualBranch === "ECONOMICS" ? 'none' : 'block';
        if (selectedDualBranch === "ECONOMICS") {
            document.getElementById("finance").value = '0';
        }
    }

    createRatingGroup(code, name) {
        const div = document.createElement('div');
        div.className = 'rating-item';

        const id = `rating-${code.toLowerCase()}`;
        div.innerHTML = `
            <label for="${id}" title="${name}">${name}:</label>
            <select id="${id}" name="${code}" required>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </select>
        `;

        return div;
    }

    async handleSubmit(event) {
        event.preventDefault();

        const formData = new FormData(this.form);

        const selectedLanguages = Array.from(
            document.querySelectorAll('input[name="programmingLanguages"]:checked')
        ).map(input => input.value);

        formData.append('selectedLanguages', selectedLanguages.join(','));

        try {
            const response = await this.submitForm(formData);
            this.handleResponse(response);
        } catch (error) {
            this.handleError(error);
        }
    }

    async submitForm(formData) {
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    handleResponse(data) {
        if (!data.success) {
            throw new Error(data.error || 'Unknown error occurred');
        }

        this.results.style.display = 'block';
        this.topMinorsList.innerHTML = Object.entries(data.top_5_minors)
            .map(([minor, score]) => `<li>${minor} (${score}%)</li>`)
            .join('');
    }

    handleError(error) {
        console.error('An error occurred:', error);
        alert('An error occurred while submitting the form. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', () => new MinorFinder());
