import pandas as pd

# 1. Read the parquet file
print("Reading parquet file...")
df = pd.read_parquet("data/Syn-training.parquet")

# 2. Save it as the specific CSV filename your PDF expects
print("Converting to CSV (this may take a minute)...")
# CORRECTED LINE BELOW:
df.to_csv("data/cicddos2019.csv", index=False)

print("Done! You now have 'data/cicddos2019.csv' ready for the PDF code.")