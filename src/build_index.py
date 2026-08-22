# ============================================================
# E-commerce Product Review Information Retrieval
# Step 3 - TF-IDF Index Construction
# ============================================================

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer


print("=" * 60)
print("E-COMMERCE REVIEW IR - TF-IDF INDEX")
print("=" * 60)


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

input_file = "data/processed_reviews.csv"

vectorizer_file = "data/tfidf_vectorizer.pkl"

matrix_file = "data/tfidf_matrix.pkl"


# ------------------------------------------------------------
# 2. Load processed reviews
# ------------------------------------------------------------

print("\nLoading processed reviews...")

df = pd.read_csv(input_file)

print(f"Reviews loaded: {len(df)}")


# ------------------------------------------------------------
# 3. Handle missing values
# ------------------------------------------------------------

df["processed_text"] = df["processed_text"].fillna("")


# ------------------------------------------------------------
# 4. Create TF-IDF Vectorizer
# ------------------------------------------------------------

print("\nCreating TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 2),
    sublinear_tf=True
)


# ------------------------------------------------------------
# 5. Convert reviews into TF-IDF matrix
# ------------------------------------------------------------

print("\nBuilding TF-IDF matrix...")

tfidf_matrix = vectorizer.fit_transform(
    df["processed_text"]
)


# ------------------------------------------------------------
# 6. Display information
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TF-IDF INDEX CREATED")
print("=" * 60)

print(
    f"\nNumber of reviews: {tfidf_matrix.shape[0]}"
)

print(
    f"Number of features: {tfidf_matrix.shape[1]}"
)

print(
    f"Matrix shape: {tfidf_matrix.shape}"
)


# ------------------------------------------------------------
# 7. Save vectorizer
# ------------------------------------------------------------

print("\nSaving TF-IDF vectorizer...")

joblib.dump(
    vectorizer,
    vectorizer_file
)


# ------------------------------------------------------------
# 8. Save TF-IDF matrix
# ------------------------------------------------------------

print("Saving TF-IDF matrix...")

joblib.dump(
    tfidf_matrix,
    matrix_file
)


# ------------------------------------------------------------
# 9. Show sample vocabulary
# ------------------------------------------------------------

print("\nSample vocabulary:")

features = vectorizer.get_feature_names_out()

print(
    features[:30]
)


# ------------------------------------------------------------
# 10. Final information
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("INDEX BUILDING COMPLETED")
print("=" * 60)

print(
    f"\nVectorizer saved to:"
    f"\n{vectorizer_file}"
)

print(
    f"\nTF-IDF matrix saved to:"
    f"\n{matrix_file}"
)

print("\n" + "=" * 60)