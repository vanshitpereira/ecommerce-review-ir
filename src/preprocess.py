# ============================================================
# E-commerce Product Review Information Retrieval
# Step 2 - Text Preprocessing
# ============================================================

import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


print("=" * 60)
print("E-COMMERCE REVIEW IR - TEXT PREPROCESSING")
print("=" * 60)


# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

input_file = "data/reviews.csv"
output_file = "data/processed_reviews.csv"

print("\nLoading dataset...")

df = pd.read_csv(input_file)

print(f"Reviews loaded: {len(df)}")


# ------------------------------------------------------------
# 2. Download/check NLTK resources
# ------------------------------------------------------------

print("\nPreparing NLP resources...")

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


# ------------------------------------------------------------
# 3. Text preprocessing function
# ------------------------------------------------------------

def preprocess_text(text):

    # Convert to string
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Keep only English alphabets and spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

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

    # Convert tokens back to text
    cleaned_text = " ".join(tokens)

    return cleaned_text


# ------------------------------------------------------------
# 4. Apply preprocessing
# ------------------------------------------------------------

print("\nPreprocessing reviews...")

df["processed_text"] = df["review_text"].apply(
    preprocess_text
)


# ------------------------------------------------------------
# 5. Remove empty reviews
# ------------------------------------------------------------

before = len(df)

df = df[
    df["processed_text"].str.strip() != ""
]

after = len(df)

print(
    f"Removed {before - after} empty reviews."
)


# ------------------------------------------------------------
# 6. Save processed dataset
# ------------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 7. Display examples
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETED")
print("=" * 60)

print(f"\nSaved to: {output_file}")

print(f"Number of reviews: {len(df)}")

print("\nColumns:")

print(df.columns.tolist())


print("\n" + "-" * 60)
print("BEFORE vs AFTER PREPROCESSING")
print("-" * 60)


for i in range(min(5, len(df))):

    print("\nOriginal:")
    print(df.iloc[i]["review_text"])

    print("\nProcessed:")
    print(df.iloc[i]["processed_text"])

    print("-" * 60)


print("\nMissing values:")

print(df.isnull().sum())

print("\n" + "=" * 60)