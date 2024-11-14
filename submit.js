class MinorFinder {
    constructor() {
        this.branchSelect = document.getElementById('branch');
        this.dualBranchSelect = document.getElementById('dualBranch');
        this.branchRatingsDiv = document.getElementById('branchRatings');
        this.financeDiv = document.getElementById('financeDiv');
        this.form = document.getElementById('surveyForm');
        this.results = document.getElementById('results');
        this.topMinorsList = document.getElementById('topMinors');
        
        // All possible branches for ratings
        this.branches = [
            "CSE", "ECE", "EEE", "ENI", "MECHANICAL", 
            "CHEMICAL", "CIVIL", "ECONOMICS", "MATHEMATICS", 
            "PHYSICS", "CHEMISTRY", "BIOLOGY"
        ];
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Initialize on page load
        this.updateBranchRatings();
        
        // Add event listeners
        this.branchSelect.addEventListener('change', () => this.updateBranchRatings());
        this.dualBranchSelect.addEventListener('change', (e) => {
            this.updateBranchRatings();
            this.handleFinanceVisibility(e);
        });
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    updateBranchRatings() {
        const selectedBranch = this.branchSelect.value;
        const selectedDualBranch = this.dualBranchSelect.value;
        
        // Clear existing content
        this.branchRatingsDiv.innerHTML = '<h3>Rate your interest in other branches (0-5):</h3>';
        
        // Create container for ratings
        const ratingsContainer = document.createElement('div');
        ratingsContainer.className = 'ratings-container';

        // Filter and create rating inputs
        this.branches.forEach(branch => {
            // Skip if branch is selected as main or dual branch
            if (branch !== selectedBranch && 
                branch !== selectedDualBranch && 
                branch !== "MnC" && 
                branch !== "PHARMACY") {
                
                const ratingDiv = document.createElement('div');
                ratingDiv.className = 'rating-item';
                
                ratingDiv.innerHTML = `
                    <label for="rating_${branch}">${branch}:</label>
                    <input 
                        type="number" 
                        id="rating_${branch}"
                        name="${branch}"
                        min="0"
                        max="5"
                        value="0"
                        required
                    >
                `;
                
                ratingsContainer.appendChild(ratingDiv);
            }
        });

        this.branchRatingsDiv.appendChild(ratingsContainer);
    }

    handleFinanceVisibility(event) {
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
            const response = await fetch('/api/submit', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                this.results.style.display = 'block';
                this.topMinorsList.innerHTML = '';
                
                Object.entries(data.top_5_minors).forEach(([minor, score]) => {
                    const li = document.createElement('li');
                    li.textContent = `${minor} (${score}%)`;
                    this.topMinorsList.appendChild(li);
                });
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            alert(`Error submitting form: ${error.message}`);
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const minorFinder = new MinorFinder();
});
