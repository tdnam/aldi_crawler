import pandas as pd

df = pd.read_csv('Aldi.csv')
df = df.sort_values(by=['category'])
df.reset_index()
df.drop_duplicates(inplace=True)
df = df.fillna("N/A")
df.to_csv('Aldi.csv', index=False)