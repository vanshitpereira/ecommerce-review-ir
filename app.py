from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import re
import nltk

from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ==================================================
# FLASK APPLICATION
# ==================================================

app = Flask(__name__)


# ==================================================
# FILE PATHS
# ==================================================

DATA_FILE = "data/processed_reviews.csv"
VECTORIZER_FILE = "data/tfidf_vectorizer.pkl"
MATRIX_FILE = "data/tfidf_matrix.pkl"


# ==================================================
# LOAD DATA
# ==================================================

reviews = pd.read_csv(DATA_FILE)

vectorizer = joblib.load(VECTORIZER_FILE)

tfidf_matrix = joblib.load(MATRIX_FILE)


# ==================================================
# NLP SETUP
# ==================================================

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


# ==================================================
# QUERY PREPROCESSING
# ==================================================

def preprocess_query(query):

    # ----------------------------------------------
    # Convert to lowercase
    # ----------------------------------------------

    query = query.lower()


    # ----------------------------------------------
    # Remove URLs
    # ----------------------------------------------

    query = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        query
    )


    # ----------------------------------------------
    # Keep only alphabets and spaces
    # ----------------------------------------------

    query = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        query
    )


    # ----------------------------------------------
    # Remove extra spaces
    # ----------------------------------------------

    query = re.sub(
        r"\s+",
        " ",
        query
    ).strip()


    # ----------------------------------------------
    # Tokenization
    # ----------------------------------------------

    tokens = query.split()


    # ----------------------------------------------
    # Stopword Removal
    # ----------------------------------------------

    tokens = [
        word
        for word in tokens
        if word not in stop_words
    ]


    # ----------------------------------------------
    # Lemmatization
    # ----------------------------------------------

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]


    # ----------------------------------------------
    # Convert tokens back to sentence
    # ----------------------------------------------

    return " ".join(tokens)


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# SEARCH API
# ==================================================

@app.route("/search")
def search():

    # ----------------------------------------------
    # GET USER QUERY
    # ----------------------------------------------

    query = request.args.get(
        "q",
        ""
    ).strip()


    # ----------------------------------------------
    # GET RATING FILTER
    # ----------------------------------------------

    rating_filter = request.args.get(
        "rating",
        "all"
    )


    # ----------------------------------------------
    # GET SORT OPTION
    # ----------------------------------------------

    sort_by = request.args.get(
        "sort",
        "relevance"
    )


    # ----------------------------------------------
    # CHECK EMPTY QUERY
    # ----------------------------------------------

    if not query:

        return jsonify({

            "results": [],

            "message":
            "Please enter a search query."

        })


    # ----------------------------------------------
    # PREPROCESS QUERY
    # ----------------------------------------------

    processed_query = preprocess_query(
        query
    )


    # ----------------------------------------------
    # CHECK EMPTY PROCESSED QUERY
    # ----------------------------------------------

    if not processed_query:

        return jsonify({

            "results": [],

            "message":
            "Please enter meaningful search words."

        })


    # ==================================================
    # TF-IDF QUERY VECTOR
    # ==================================================

    query_vector = vectorizer.transform(
        [processed_query]
    )


    # ==================================================
    # COSINE SIMILARITY
    # ==================================================

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()


    # ==================================================
    # CREATE RESULT LIST
    # ==================================================

    results = []


    # ==================================================
    # PROCESS ALL REVIEWS
    # ==================================================

    for index, score in enumerate(similarities):


        # ----------------------------------------------
        # Ignore reviews with zero similarity
        # ----------------------------------------------

        if score <= 0:

            continue


        # ----------------------------------------------
        # Get review
        # ----------------------------------------------

        review = reviews.iloc[index]


        # ----------------------------------------------
        # Get numeric rating
        # ----------------------------------------------

        try:

            numeric_rating = float(
                review["rating"]
            )

        except:

            numeric_rating = 0


        # ==================================================
        # RATING FILTER
        # ==================================================

        if rating_filter != "all":

            if numeric_rating != float(
                rating_filter
            ):

                continue


        # ==================================================
        # ADD RESULT
        # ==================================================

        results.append({

            "review_id": str(
                review["review_id"]
            ),

            "review_text": str(
                review["review_text"]
            ),

            "rating": numeric_rating,

            "rating_text": str(
                review["rating_text"]
            ),

            "similarity": float(
                score
            )

        })


    # ==================================================
    # SORT RESULTS
    # ==================================================

    if sort_by == "rating":

        # Sort by rating
        # Highest rating first

        results.sort(

            key=lambda x: x["rating"],

            reverse=True

        )

    else:

        # Default sorting:
        # Highest relevance first

        results.sort(

            key=lambda x: x["similarity"],

            reverse=True

        )


    # ==================================================
    # GET TOP 5 RESULTS
    # ==================================================

    results = results[:10]


    # ==================================================
    # ADD RANK
    # ==================================================

    for i, result in enumerate(results):

        result["rank"] = i + 1


        result["similarity"] = round(

            result["similarity"],

            4

        )


    # ==================================================
    # NO RESULTS
    # ==================================================

    if not results:

        return jsonify({

            "results": [],

            "message":
            "No relevant reviews found for the selected filters."

        })


    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return jsonify({

        "results": results,

        "query": query,

        "processed_query": processed_query,

        "rating_filter": rating_filter,

        "sort_by": sort_by

    })


# ==================================================
# RUN FLASK SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )