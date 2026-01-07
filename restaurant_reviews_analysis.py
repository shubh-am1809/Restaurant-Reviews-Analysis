import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import os

df = pd.read_csv("dataset .csv")
df = df[['Rating text', 'Aggregate rating']].dropna()

positive_reviews = df[df['Aggregate rating'] >= 4]['Rating text']
negative_reviews = df[df['Aggregate rating'] <= 2]['Rating text']

positive_words = Counter(" ".join(positive_reviews).lower().split())
negative_words = Counter(" ".join(negative_reviews).lower().split())

top_positive = positive_words.most_common(5)
top_negative = negative_words.most_common(5)

df['review_length'] = df['Rating text'].apply(lambda x: len(x.split()))
average_length = df['review_length'].mean()
rating_vs_length = df.groupby('Aggregate rating')['review_length'].mean()

os.makedirs("output", exist_ok=True)
pd.DataFrame(top_positive, columns=['Word', 'Frequency']) \
    .to_csv("output/top_positive_keywords.csv", index=False)
pd.DataFrame(top_negative, columns=['Word', 'Frequency']) \
    .to_csv("output/top_negative_keywords.csv", index=False)
rating_vs_length.reset_index().to_csv(
    "output/review_length_vs_rating.csv", index=False
)

plt.figure()
plt.plot(rating_vs_length.index, rating_vs_length.values, marker='o')
plt.xlabel("Rating")
plt.ylabel("Average Text Length")
plt.title("Rating Text Length vs Rating")
plt.tight_layout()
plt.savefig("output/review_length_vs_rating.png")
plt.close()

print("\nTop Positive Keywords:", top_positive)
print("Top Negative Keywords:", top_negative)
print(f"Average Text Length: {average_length:.2f} words")
print("Outputs saved in output/ folder")
