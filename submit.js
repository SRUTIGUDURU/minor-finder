// submit.js

const branchSelect = document.getElementById('branch');
const dualBranchSelect = document.getElementById('dualBranch');
const branchRatingsDiv = document.getElementById('branchRatings');
const financeDiv = document.getElementById('financeDiv');
const form = document.getElementById('surveyForm');

function updateBranchRatings() {
    const selectedBranch = branchSelect.value;
    const selectedDualBranch = dualBranchSelect.value;
    const branches = ["CSE", "ECE", "EEE", "ENI", "MECHANICAL", "CHEMICAL", "CIVIL", "ECONOMICS", "MATHEMATICS", "PHYSICS", "CHEMISTRY", "BIOLOGY"];
    
    branchRatingsDiv.innerHTML = '';
    const excludedBranches = new Set(["MnC", "PHARMACY", selectedBranch, selectedDualBranch]);

    branches.forEach(branch => {
        if (!excludedBranches.has(branch)) {
            const div = document.createElement('div');
            div.innerHTML = `<label>${branch}</label><input type="number" name="${branch}" min="0" max="5" value="0" required>`;
            branchRatingsDiv.appendChild(div);
        }
    });
}

branchSelect.addEventListener('change', updateBranchRatings);
dualBranchSelect.addEventListener('change', (e) => {
    updateBranchRatings();
    financeDiv.style.display = e.target.value === "ECONOMICS" ? 'none' : 'block';
    if (e.target.value === "ECONOMICS") {
        document.querySelector('input[name="Finance"]').value = '0';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    updateBranchRatings();
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    // Collect selected programming languages
    const selectedLanguages = Array.from(document.querySelectorAll('input[name="programmingLanguages"]:checked'))
        .map(input => input.value)
        .join(", ");
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
            topMinorsList.innerHTML = '';

            Object.entries(data.top_5_minors).forEach(([minor, score]) => {
                const li = document.createElement('li');
                li.textContent = `${minor} (${score}%)`;
                topMinorsList.appendChild(li);
            });
        } else {
            alert('Error processing form: ' + data.error);
        }
    } catch (error) {
        alert('Error submitting form: ' + error);
    }
});
