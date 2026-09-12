// =========================================
// GET HTML ELEMENTS
// =========================================

const searchInput = document.getElementById("searchInput");

const searchButton = document.getElementById("searchButton");

const resultsContainer =
    document.getElementById("resultsContainer");

const resultsTitle =
    document.getElementById("resultsTitle");

const resultsInfo =
    document.getElementById("resultsInfo");

const loading =
    document.getElementById("loading");

const noResults =
    document.getElementById("noResults");


// =========================================
// SEARCH FUNCTION
// =========================================

async function searchReviews() {

    // Get query
    const query = searchInput.value.trim();


    // Check empty query
    if (!query) {

        alert("Please enter a search query.");

        return;
    }


    // Show loading
    loading.classList.remove("hidden");

    noResults.classList.add("hidden");

    resultsContainer.innerHTML = "";


    resultsTitle.textContent = "Searching...";

    resultsInfo.textContent =
        "Finding relevant reviews.";


    try {

        // Send request to Flask
        const response = await fetch(
            `/search?q=${encodeURIComponent(query)}`
        );


        // Convert response to JSON
        const data = await response.json();


        // Hide loading
        loading.classList.add("hidden");


        // Check results
        if (!data.results || data.results.length === 0) {

            resultsTitle.textContent =
                "No Results";

            resultsInfo.textContent =
                data.message ||
                "No relevant reviews found.";

            noResults.classList.remove("hidden");

            return;
        }


        // Update heading
        resultsTitle.textContent =
            "Search Results";


        resultsInfo.textContent =
            `Top ${data.results.length} relevant reviews for "${query}"`;


        // Display results
        displayResults(data.results);


    }

    catch (error) {

        console.error(error);


        loading.classList.add("hidden");


        resultsTitle.textContent =
            "Error";


        resultsInfo.textContent =
            "Unable to retrieve search results.";


        noResults.classList.remove("hidden");

    }

}


// =========================================
// DISPLAY RESULTS
// =========================================

function displayResults(results) {

    resultsContainer.innerHTML = "";


    results.forEach(function(review) {


        // Create review card
        const card =
            document.createElement("div");


        card.className =
            "review-card";


        // Convert similarity to percentage
        const relevance =
            (review.similarity * 100).toFixed(2);


        // Create card HTML
        card.innerHTML = `

            <div class="review-top">

                <span class="rank">
                    Result #${review.rank}
                </span>

                <span class="score">
                    Relevance: ${relevance}%
                </span>

            </div>


            <div class="review-text">

                ${escapeHTML(review.review_text)}

            </div>


            <div class="review-details">

                <span class="rating">

                    ⭐ ${escapeHTML(review.rating_text)}

                </span>

                <span class="review-id">

                    Review ID: ${escapeHTML(review.review_id)}

                </span>

            </div>

        `;


        // Add card to page
        resultsContainer.appendChild(card);

    });

}


// =========================================
// HTML ESCAPE FUNCTION
// =========================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// =========================================
// SEARCH BUTTON
// =========================================

searchButton.addEventListener(
    "click",
    searchReviews
);


// =========================================
// ENTER KEY SEARCH
// =========================================

searchInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            searchReviews();

        }

    }
);


// =========================================
// EXAMPLE SEARCH BUTTONS
// =========================================

const exampleButtons =
    document.querySelectorAll(".example-btn");


exampleButtons.forEach(function(button) {

    button.addEventListener(
        "click",
        function() {

            searchInput.value =
                button.textContent.trim();

            searchReviews();

        }
    );

});