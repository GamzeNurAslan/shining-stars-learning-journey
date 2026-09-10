import pandas as pd

df = pd.read_csv("gonderiler_faker.csv", encoding="utf-8-sig")

print("\n--- ILK 5 SATIR ---")
print(df.head())

print("\n--- BOYUT ---")
print(df.shape)

print("\n--- SUTUNLAR ---")
print(df.columns.tolist())

print("\n--- VERI TIPLERI VE DOLULUK ---")
df.info()

print("\n--- EKSIK DEGERLER ---")
print(df.isnull().sum())

print("\n--- SAYISAL OZET ---")
print(df.describe())

print("\n--- TEKRAR EDEN SATIR SAYISI ---")
print(df.duplicated().sum())