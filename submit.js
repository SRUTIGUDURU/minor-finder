class MinorFinder {
    constructor() {
        this.branchSelect = document.getElementById('branch');
        this.dualBranchSelect = document.getElementById('dualBranch');
        this.branchRatingsDiv = document.getElementById('branchRatings');
        this.financeDiv = document.getElementById('financeDiv');
        this.form = document.getElementById('surveyForm');
        
        // All possible branches that can be rated
        this.allBranches = [
            "CSE", "ECE", "EEE", "ENI", "MECHANICAL", 
            "CHEMICAL", "CIVIL", "ECONOMICS", "MATHEMATICS", 
            "PHYSICS", "CHEMISTRY", "BIOLOGY"
        ];
        
        this.initializeEventListeners();
        this.initializeBranchRatings(); // Initialize on page load
    }

    initializeEventListeners() {
        this.branchSelect.addEventListener('change', () => this.updateBranchRatings());
        this.dualBranchSelect.addEventListener('change', (e) => this.handleDualBranchChange(e));
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    initializeBranchRatings() {
        // Create initial branch ratings section
        this.branchRatingsDiv.innerHTML = '<h2>Rate your interest in other branches (0-5):</h2><div class="ratings-container"></div>';
        this.updateBranchRatings();
    }

    getVisibleBranches() {
        const selectedBranch = this.branchSelect.value;
        const selectedDualBranch = this.dualBranchSelect.value;
        
        // Start with all branches
        let visibleBranches = [...this.allBranches];
        
        // Remove selected branch and dual branch
        visibleBranches = visibleBranches.filter(branch => 
            branch !== selectedBranch && 
            branch !== selectedDualBranch
        );
        
        // Special handling for MnC
        if (selectedBranch === "MnC") {
            visibleBranches = visibleBranches.filter(branch => 
                branch !== "CSE" && 
                branch !== "MATHEMATICS"
            );
        }
        
        // Remove PHARMACY from ratings (as it's not in the rating system)
        visibleBranches = visibleBranches.filter(branch => branch !== "PHARMACY");
        
        return visibleBranches;
    }

    updateBranchRatings() {
        const container = this.branchRatingsDiv.querySelector('.ratings-container');
        const visibleBranches = this.getVisibleBranches();
        
        // Save existing values
        const existingValues = {};
        container.querySelectorAll('select').forEach(select => {
            existingValues[select.name] = select.value;
        });
        
        // Create the new ratings HTML
        container.innerHTML = visibleBranches.map(branch => {
            const value = existingValues[branch] || "0";
            return `
                <div class="rating-item">
                    <label for="rating-${branch}">${branch}:</label>
                    <select id="rating-${branch}" name="${branch}" required>
                        ${[0, 1, 2, 3, 4, 5].map(num => 
                            `<option value="${num}" ${value === num.toString() ? 'selected' : ''}>${num}</option>`
                        ).join('')}
                    </select>
                </div>
            `;
        }).join('');
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
            const response = await fetch('/api/submit', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('results').style.display = 'block';
                const topMinorsList = document.getElementById('topMinors');
                topMinorsList.innerHTML = Object.entries(data.top_5_minors)
                    .map(([minor, score]) => `<li>${minor} (${score}%)</li>`)
                    .join('');
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            alert(`Error submitting form: ${error.message}`);
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const minorFinder = new MinorFinder();
});
