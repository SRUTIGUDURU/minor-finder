class MinorFinder {
    constructor() {
        this.branchSelect = document.getElementById('branch');
        this.dualBranchSelect = document.getElementById('dualBranch');
        this.branchRatingsDiv = document.getElementById('branchRatings');
        this.financeDiv = document.getElementById('financeDiv');
        this.form = document.getElementById('surveyForm');
        this.results = document.getElementById('results');
        this.topMinorsList = document.getElementById('topMinors');
        
        this.branches = [
            "CSE", "ECE", "EEE", "ENI", "MECHANICAL", 
            "CHEMICAL", "CIVIL", "ECONOMICS", "MATHEMATICS", 
            "PHYSICS", "CHEMISTRY", "BIOLOGY"
        ];
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.branchSelect.addEventListener('change', () => this.updateBranchRatings());
        this.dualBranchSelect.addEventListener('change', (e) => this.handleDualBranchChange(e));
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        document.addEventListener('DOMContentLoaded', () => this.updateBranchRatings());
    }

    updateBranchRatings() {
        const selectedBranch = this.branchSelect.value;
        const selectedDualBranch = this.dualBranchSelect.value;
        const excludedBranches = new Set(["MnC", "PHARMACY", selectedBranch, selectedDualBranch]);

        const ratingInputs = this.branches
            .filter(branch => !excludedBranches.has(branch))
            .map(branch => this.createRatingInput(branch));

        this.branchRatingsDiv.innerHTML = '<h2>Rate your interest in other branches (0-5):</h2>';
        ratingInputs.forEach(input => this.branchRatingsDiv.appendChild(input));
    }

    createRatingInput(branch) {
        const div = document.createElement('div');
        div.className = 'rating-item';
        const id = `rating-${branch.toLowerCase()}`;
        
        div.innerHTML = `
            <label for="${id}">${branch}:</label>
            <input type="number" 
                   id="${id}"
                   name="${branch}"
                   min="0"
                   max="5"
                   value="0"
                   required>
        `;
        return div;
    }

    handleDualBranchChange(event) {
        this.updateBranchRatings();
        const isEconomics = event.target.value === "ECONOMICS";
        this.financeDiv.style.display = isEconomics ? 'none' : 'block';
        if (isEconomics) {
            document.querySelector('input[name="Finance"]').value = '0';
        }
    }

    async handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(this.form);
        
        // Add selected programming languages
        const selectedLanguages = Array.from(
            document.querySelectorAll('input[name="programmingLanguages"]:checked')
        ).map(input => input.value).join(", ");
        formData.append('selectedLanguages', selectedLanguages);

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
        console.error('Form submission error:', error);
        alert(`Error submitting form: ${error.message}`);
    }
}

// Initialize the application
const minorFinder = new MinorFinder();
