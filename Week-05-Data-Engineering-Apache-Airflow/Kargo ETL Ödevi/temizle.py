import pandas as pd

df = pd.read_csv("gonderiler_faker.csv", encoding="utf-8-sig")

print("Baslangic satir sayisi:", len(df))

# 1) Birebir ayni tekrar eden satirlari sil
df = df.drop_duplicates()

print("Duplicate temizligi sonrasi:", len(df))

# 2) Sehir isimlerindeki bosluklari temizle
df["alici_sehir"] = df["alici_sehir"].astype("string").str.strip()

# Turkce I / İ problemi icin kontrollu esleme
sehir_duzeltmeleri = {
    "ISTANBUL": "İstanbul",
    "İSTANBUL": "İstanbul",
    "Istanbul": "İstanbul",
    "istanbul": "İstanbul",
    "İstanbul": "İstanbul",

    "IZMIR": "İzmir",
    "izmir": "İzmir",
    "İzmir": "İzmir",

    "ANKARA": "Ankara",
    "ankara": "Ankara",
    "Ankara": "Ankara",

    "BURSA": "Bursa",
    "bursa": "Bursa",
    "Bursa": "Bursa",
}

df["alici_sehir"] = df["alici_sehir"].replace(sehir_duzeltmeleri)

# 3) Durum alanini standart hale getir
df["durum"] = df["durum"].astype("string").str.strip().str.lower()

# Normalizasyon sonrasinda ayni hale gelen kayitlari da temizle
df = df.drop_duplicates()

# 4) Tarihleri datetime tipine cevir
df["kabul_tarihi"] = pd.to_datetime(
    df["kabul_tarihi"],
    errors="coerce"
)

df["teslim_tarihi"] = pd.to_datetime(
    df["teslim_tarihi"],
    errors="coerce"
)

# 5) Karantina nedenini tutacagimiz kolon
df["karantina_nedeni"] = ""

df.loc[
    df["alici_sehir"].isna(),
    "karantina_nedeni"
] += "alici_sehir_eksik;"

df.loc[
    df["agirlik_kg"].isna(),
    "karantina_nedeni"
] += "agirlik_eksik;"

df.loc[
    df["agirlik_kg"].notna() & (df["agirlik_kg"] <= 0),
    "karantina_nedeni"
] += "agirlik_gecersiz;"

df.loc[
    df["kabul_tarihi"].isna(),
    "karantina_nedeni"
] += "kabul_tarihi_gecersiz;"

df.loc[
    (df["durum"] == "teslim") &
    df["teslim_tarihi"].isna(),
    "karantina_nedeni"
] += "teslim_tarihi_eksik;"

df.loc[
    (df["durum"] == "teslim") &
    df["teslim_tarihi"].notna() &
    df["kabul_tarihi"].notna() &
    (df["teslim_tarihi"] < df["kabul_tarihi"]),
    "karantina_nedeni"
] += "teslim_kabulden_once;"

# 6) Temiz ve problemli veriyi ayir
karantina = df[df["karantina_nedeni"] != ""].copy()

temiz = df[df["karantina_nedeni"] == ""].copy()
temiz = temiz.drop(columns=["karantina_nedeni"])

# 7) Sonuclari CSV olarak kaydet
temiz.to_csv(
    "gonderiler_temiz.csv",
    index=False,
    encoding="utf-8-sig"
)

karantina.to_csv(
    "gonderiler_karantina.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nTemiz veri satir sayisi:", len(temiz))
print("Karantinaya ayrilan:", len(karantina))

print("\nKarantina nedenleri:")
print(karantina["karantina_nedeni"].value_counts())

print("\nSehirler:")
print(sorted(temiz["alici_sehir"].unique()))

print("\nDurumlar:")
print(sorted(temiz["durum"].unique()))