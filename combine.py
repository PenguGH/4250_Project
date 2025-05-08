import pandas as pd

# Load retrieval scores
df_0 = pd.read_csv("./improved_retrieval/retrieval_output_0.csv")
df_0["Query"] = "baseball magic airplane"
df_1 = pd.read_csv("./improved_retrieval/retrieval_output_1.csv")
df_1["Query"] = "camera smartphone gaming"
df_2 = pd.read_csv("./improved_retrieval/retrieval_output_2.csv")
df_2["Query"] = "computer banana ocean"

# Combine them into one DataFrame
retrieval_all = pd.concat([df_0, df_1, df_2], ignore_index=True)

# Ensure 'Document Name' is string for matching
retrieval_all["Document Name"] = retrieval_all["Document Name"].astype(str)

# Load map
doc_map = pd.read_csv("doc_url_map.csv")
doc_map["Document Name"] = doc_map["Document Name"].astype(str)

# Load PageRank scores 
pagerank_df = pd.read_csv("pagerank_all_pages.csv")
pagerank_df["URL"] = pagerank_df["URL"].astype(str)

# Merge retrieval with URL mapping 
retrieval_with_url = pd.merge(retrieval_all, doc_map, on="Document Name", how="left")

# Merge with PageRank
combined = pd.merge(retrieval_with_url, pagerank_df, on="URL", how="inner")

# Calculate Final Score 
combined["Final Score"] = combined["Cosine Similarity"] * combined["PageRank"]

# Sort results from highest to lowest final ranked
combined_sorted = combined.sort_values(by="Final Score", ascending=False)

# Final rank group by query
combined_sorted["Final Rank"] = combined_sorted.groupby("Query")["Final Score"].rank(method="first", ascending=False).astype(int)

# Format to make it clear
combined_sorted = combined_sorted[
    ["Query", "Final Rank", "Document Name", "URL", "Cosine Similarity", "PageRank", "Final Score"]
]

combined_sorted["Cosine Similarity"] = combined_sorted["Cosine Similarity"].round(4)
combined_sorted["PageRank"] = combined_sorted["PageRank"].apply(lambda x: f"{x:.2e}")
combined_sorted["Final Score"] = combined_sorted["Final Score"].apply(lambda x: f"{x:.2e}")



combined_sorted.to_csv("final_combined_scores.csv", index=False)
print("Combined scores saved to 'final_combined_scores.csv'")
