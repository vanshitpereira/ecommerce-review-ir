import json
import pandas as pd
import os
import urllib.request

print("=" * 60)
print("Amazon Reviews Multi - Dataset Preparation")
print("=" * 60)

# ---------------------------------------------------------
# 1. Dataset URL
# ---------------------------------------------------------

url = "https://huggingface.co/datasets/mteb/amazon_reviews_multi/resolve/main/en/train.jsonl"

raw_file = "data/train.jsonl"
output_file = "data/reviews.csv"

os.makedirs("data", exist_ok=True)

# ---------------------------------------------------------
# 2. Download dataset if it doesn't already exist
# ---------------------------------------------------------

if not os.path.exists(raw_file):

    print("\nDownloading English Amazon Reviews dataset...")
    print("This file is approximately 53 MB.")

    urllib.request.urlretrieve(
        url,
        raw_file
    )

    print("Download completed!")

else:

    print("\nDataset file already exists.")
    print("Skipping download.")

# ---------------------------------------------------------
# 3. Read JSONL
# ---------------------------------------------------------

print("\nReading dataset...")

records = []

with open(
    raw_file,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        if line.strip():

            records.append(
                json.loads(line)
            )

print(
    f"Total reviews loaded: {len(records)}"
)

# ---------------------------------------------------------
# 4. Convert to Pandas
# ---------------------------------------------------------

df = pd.DataFrame(records)

print("\nAvailable columns:")
print(df.columns.tolist())

# ---------------------------------------------------------
# 5. Rename columns for our project
# ---------------------------------------------------------

df = df.rename(
    columns={
        "id": "review_id",
        "text": "review_text",
        "label": "rating",
        "label_text": "rating_text"
    }
)

# ---------------------------------------------------------
# 6. Keep only the fields we need
# ---------------------------------------------------------

df = df[
    [
        "review_id",
        "review_text",
        "rating",
        "rating_text"
    ]
]

# ---------------------------------------------------------
# 7. Remove missing reviews
# ---------------------------------------------------------

before = len(df)

df = df.dropna(
    subset=["review_text"]
)

after = len(df)

print(
    f"\nRemoved {before - after} reviews with missing text."
)

# ---------------------------------------------------------
# 8. Select 30,000 reviews
# ---------------------------------------------------------

SAMPLE_SIZE = 30000

if len(df) < SAMPLE_SIZE:

    raise ValueError(
        f"Only {len(df)} reviews available."
    )

df = df.sample(
    n=SAMPLE_SIZE,
    random_state=42
)

# ---------------------------------------------------------
# 9. Reset index
# ---------------------------------------------------------

df = df.reset_index(
    drop=True
)

# ---------------------------------------------------------
# 10. Save dataset
# ---------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# 11. Display information
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DATASET PREPARATION COMPLETED")
print("=" * 60)

print(
    f"\nSaved to: {output_file}"
)

print(
    f"Number of reviews: {len(df)}"
)

print(
    f"Number of columns: {len(df.columns)}"
)

print("\nFinal columns:")

print(
    df.columns.tolist()
)

print("\nFirst 5 reviews:")

print(
    df.head()
)

print("\nRating distribution:")

print(
    df["rating_text"].value_counts()
)

print("\nMissing values:")

print(
    df.isnull().sum()
)

print("\n" + "=" * 60)