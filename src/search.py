# ============================================================
# E-commerce Product Review Information Retrieval
# Step 4 - Search Engine
# ============================================================

import re
import joblib
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.metrics.pairwise import cosine_similarity


print("=" * 60)
print("E-COMMERCE REVIEW INFORMATION RETRIEVAL")
print("SEARCH ENGINE")
print("=" * 60)


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_FILE = "data/processed_reviews.csv"

VECTORIZER_FILE = "data/tfidf_vectorizer.pkl"

MATRIX_FILE = "data/tfidf_matrix.pkl"


# ------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------

print("\nLoading review dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Reviews loaded: {len(df)}")


# ------------------------------------------------------------
# 3. Load TF-IDF vectorizer
# ------------------------------------------------------------

print("Loading TF-IDF vectorizer...")

vectorizer = joblib.load(
    VECTORIZER_FILE
)


# ------------------------------------------------------------
# 4. Load TF-IDF matrix
# ------------------------------------------------------------

print("Loading TF-IDF matrix...")

tfidf_matrix = joblib.load(
    MATRIX_FILE
)


# ------------------------------------------------------------
# 5. Prepare NLP tools
# ------------------------------------------------------------

stop_words = set(
    stopwords.words("english")
)

lemmatizer = WordNetLemmatizer()


# ------------------------------------------------------------
# 6. Query preprocessing
# ------------------------------------------------------------

def preprocess_query(text):

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # Keep alphabets only
    text = re.sub(
        r"[^a-z\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # Tokenization
    tokens = text.split()

    # Remove stopwords
    tokens = [
        word
        for word in tokens
        if word not in stop_words
    ]

    # Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return " ".join(tokens)


# ------------------------------------------------------------
# 7. Search function
# ------------------------------------------------------------

def search_reviews(query, top_k=5):

    # Preprocess query
    processed_query = preprocess_query(query)

    # Check empty query
    if not processed_query:

        print("\nPlease enter a valid search query.")

        return

    # Convert query into TF-IDF vector
    query_vector = vectorizer.transform(
        [processed_query]
    )

    # Calculate cosine similarity
    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    # Get highest similarity scores
    ranked_indices = similarities.argsort()[
        ::-1
    ]

    # Display results
    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    results_found = 0

    for index in ranked_indices:

        score = similarities[index]

        # Ignore completely irrelevant results
        if score <= 0:
            continue

        results_found += 1

        print(
            f"\nResult {results_found}"
        )

        print(
            "-" * 60
        )

        print(
            f"Similarity Score: {score:.4f}"
        )

        print(
            f"Rating: {df.iloc[index]['rating_text']}"
        )

        print(
            f"\nReview:\n"
            f"{df.iloc[index]['review_text']}"
        )

        if results_found >= top_k:
            break

    if results_found == 0:

        print(
            "\nNo relevant reviews found."
        )


# ------------------------------------------------------------
# 8. Interactive search
# ------------------------------------------------------------

print("\nSearch engine ready!")

print(
    "\nEnter 'exit' to close the search engine."
)


while True:

    query = input(
        "\nEnter your search query: "
    )

    if query.lower() == "exit":

        print(
            "\nExiting search engine..."
        )

        break

    search_reviews(
        query,
        top_k=5
    )