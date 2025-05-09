// Define the filename for the CSV data
const DATA_FILENAME = 'insular_manuscripts_britain_700_1100.csv';
const MIN_YEAR = 700;
const MAX_YEAR = 1100;

// Column indices (0-based) based on the expected CSV structure
const COL_YEAR_START = 4;
const COL_YEAR_END = 5;
const COL_PLACE_BROAD = 6;
const COL_ILLUSTRATED = 9;

// Variables to store parsed data
let manuscriptData = [];

// --- Helper Functions ---

// Function to parse CSV data (basic implementation)
function parseCSV(text) {
    const lines = text.split('\n');
    const data = [];
    // Assuming the first line is a header and skipping it
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line) { // Skip empty lines
            // Basic splitting by comma - might need more robust parsing for complex CSVs
            const row = line.split(',');
            data.push(row);
        }
    }
    return data;
}

// Function to validate and parse user input (year or range)
function parseYearInput(input) {
    const rangeMatch = input.match(/^(\d{3,4})-(\d{3,4})$/);
    const yearMatch = input.match(/^(\d{3,4})$/);

    if (rangeMatch) {
        const start = parseInt(rangeMatch[1], 10);
        const end = parseInt(rangeMatch[2], 10);
        if (start >= MIN_YEAR && end <= MAX_YEAR && start <= end) {
            return { start: start, end: end, type: 'range' };
        }
    } else if (yearMatch) {
        const year = parseInt(yearMatch[1], 10);
        if (year >= MIN_YEAR && year <= MAX_YEAR) {
            return { start: year, end: year, type: 'year' };
        }
    }

    return null; // Indicates invalid input
}

// --- Core Analysis Function ---

function analyzeManuscripts(yearStart, yearEnd) {
    let totalManuscripts = 0;
    let illustratedManuscripts = 0;

    // Ensure data is loaded before attempting analysis
    if (manuscriptData.length === 0) {
        console.error("Manuscript data not loaded.");
        return { total: 0, illustrated: 0, percentage: 0, error: "Data not loaded. Please try again." };
    }

    // Iterate through the parsed data (skipping header which was already handled)
    for (const row of manuscriptData) {
        // Basic check if row has enough columns
        const requiredCols = [COL_YEAR_START, COL_YEAR_END, COL_PLACE_BROAD, COL_ILLUSTRATED];
        if (row.length <= Math.max(...requiredCols)) {
            // console.warn("Skipping row due to insufficient columns:", row);
            continue; // Skip rows that don't have the expected number of columns
        }

        try {
            const prodYearStartStr = row[COL_YEAR_START].trim();
            const prodYearEndStr = row[COL_YEAR_END].trim();
            const prodPlaceBroad = row[COL_PLACE_BROAD].trim();
            const containsIllustrationStr = row[COL_ILLUSTRATED].trim().toLowerCase();

            // Skip if essential date or place data is missing
            if (!prodYearStartStr || !prodYearEndStr || !prodPlaceBroad) {
                 // console.warn("Skipping row due to missing date or place data:", row);
                 continue;
            }

            // Convert years to integers
            const prodYearStart = parseInt(prodYearStartStr, 10);
            const prodYearEnd = parseInt(prodYearEndStr, 10);

            // Check if parsing years resulted in NaN (Not a Number)
            if (isNaN(prodYearStart) || isNaN(prodYearEnd)) {
                 // console.warn("Skipping row due to invalid year format:", row);
                 continue;
            }


            // Apply filters: Place is Britain and date ranges overlap
            if (prodPlaceBroad === "Britain" &&
                (prodYearStart <= yearEnd && prodYearEnd >= yearStart)) {

                totalManuscripts++;

                // Check illustration status (allowing variations like "true", "yes", "1")
                if (['true', 'yes', '1'].includes(containsIllustrationStr)) {
                    illustratedManuscripts++;
                }
            }
        } catch (e) {
            console.error("Error processing row:", row, e);
            // Continue to the next row even if one row causes an error
        }
    }

    const percentage = totalManuscripts > 0 ? (illustratedManuscripts / totalManuscripts) * 100 : 0;

    return {
        total: totalManuscripts,
        illustrated: illustratedManuscripts,
        percentage: percentage.toFixed(2), // Format to 2 decimal places
        error: null // No error during analysis
    };
}

// --- DOM Manipulation Functions ---

function displayResults(results, yearInput) {
    const resultsArea = document.getElementById('resultsArea');
    const resultsText = document.getElementById('resultsText');
    const errorArea = document.getElementById('errorArea');

    errorArea.classList.add('hidden'); // Hide error area
    resultsArea.classList.remove('hidden'); // Show results area

    if (results.total === 0) {
        resultsText.innerHTML = `No known extant manuscripts found matching the criteria for the period ${yearInput.start}-${yearInput.end} CE produced in Britain in the loaded data.`;
    } else {
        resultsText.innerHTML = `
            Total known extant manuscripts (Britain, ${yearInput.start}-${yearInput.end} CE): <strong>${results.total}</strong><br>
            Number of these containing illustrations/illuminations: <strong>${results.illustrated}</strong><br>
            Percentage illustrated: <strong>${results.percentage}%</strong>
        `;
    }
}

function displayError(message) {
    const resultsArea = document.getElementById('resultsArea');
    const errorArea = document.getElementById('errorArea');
    const errorText = document.getElementById('errorText');

    resultsArea.classList.add('hidden'); // Hide results area
    errorArea.classList.remove('hidden'); // Show error area
    errorText.textContent = message;
}

// --- Event Listener and Data Loading ---

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysisForm');
    const yearInput = document.getElementById('yearInput');

    // Fetch and load the CSV data when the page loads
    fetch(DATA_FILENAME)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(csvText => {
            manuscriptData = parseCSV(csvText);
            console.log(`Successfully loaded and parsed ${manuscriptData.length} data rows.`);
            // Data is loaded, form is now effectively ready
        })
        .catch(error => {
            console.error("Error fetching or parsing CSV data:", error);
            displayError(`Could not load data file (${DATA_FILENAME}). Please ensure it exists in the same directory.`);
            // Disable form or button if data loading fails critically
            form.querySelector('button').disabled = true;
            yearInput.disabled = true;
        });


    // Add event listener for form submission
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const input = yearInput.value.trim();
        const parsedInput = parseYearInput(input);

        if (!parsedInput) {
            displayError(`Invalid input: "${input}". Please enter a year (YYYY) or a year range (YYYY-YYYY) between ${MIN_YEAR} and ${MAX_YEAR}.`);
            return; // Stop if input is invalid
        }

        // If data wasn't loaded successfully, show error again
        if (manuscriptData.length === 0) {
             displayError(`Data not loaded. Cannot perform analysis. Please check the console for errors.`);
             return;
        }


        // Perform the analysis
        const results = analyzeManuscripts(parsedInput.start, parsedInput.end);

        // Display results or analysis-specific error
        if (results.error) {
            displayError(results.error);
        } else {
            displayResults(results, parsedInput);
        }
    });
});
