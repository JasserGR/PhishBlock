import pandas as pd

df = pd.read_csv('data/phishing_urls.csv')
print(df.head())
print(df.info())
print(df.shape)
print("\nClass Distribution (Result column):")
print(df['Result'].value_counts())
print("\nDescriptive Statistics:")
print(df.describe())