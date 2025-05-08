import pandas as pd

df = pd.read_csv("outlinks.csv")

# Rename the second column to 'Document Name'
df.rename(columns={"Outlinks Count": "Document Name"}, inplace=True)

# Remove ".txt" from the document names and convert to string
df["Document Name"] = df["Document Name"].str.replace(".txt", "", regex=False).astype(str)

df.to_csv("doc_url_map.csv", index=False)