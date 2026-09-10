from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker("tr_TR")

Faker.seed(42)
random.seed(42)

kayitlar = []

for i in range(5000):
    kabul = fake.date_time_between(
        start_date="-8M",
        end_date="now"
    )

    durum = random.choice(["teslim", "yolda", "iade"])

    if durum == "teslim":
        teslim = kabul + timedelta(days=random.randint(1, 7))
    else:
        teslim = None

    kayitlar.append({
        "gonderi_id": f"TR{100000 + i}",
        "sube_kodu": random.choice(["IST", "ANK", "IZM", "BUR", "ANT"]),
        "alici_sehir": fake.city(),
        "agirlik_kg": round(random.uniform(0.1, 30), 2),
        "durum": durum,
        "kabul_tarihi": kabul,
        "teslim_tarihi": teslim
    })

df = pd.DataFrame(kayitlar)

# -----------------------------
# KASITLI KIRLI VERI EKLEME
# -----------------------------

tum_indexler = list(df.index)
random.shuffle(tum_indexler)

sehir_eksik = tum_indexler[:25]
agirlik_eksik = tum_indexler[25:37]
agirlik_hatali = tum_indexler[37:77]
tarih_hatali = tum_indexler[77:97]
istanbul_yazim = tum_indexler[97:127]

# Eksik sehir
df.loc[sehir_eksik, "alici_sehir"] = None

# Eksik agirlik
df.loc[agirlik_eksik, "agirlik_kg"] = None

# Negatif / sifir agirlik
for idx in agirlik_hatali:
    df.loc[idx, "agirlik_kg"] = random.choice([-3.5, -1.2, -0.5, 0])

# Teslim tarihi kabul tarihinden once olsun
for idx in tarih_hatali:
    df.loc[idx, "durum"] = "teslim"
    df.loc[idx, "teslim_tarihi"] = (
        df.loc[idx, "kabul_tarihi"] - timedelta(days=2)
    )

# Turkce I / I ve bosluk problemi
istanbul_ornekleri = [
    "İstanbul",
    "istanbul",
    "ISTANBUL",
    " Istanbul ",
    "İSTANBUL"
]

for idx in istanbul_yazim:
    df.loc[idx, "alici_sehir"] = random.choice(istanbul_ornekleri)

# 50 tane duplicate satir ekle
duplicate_satirlar = df.sample(
    n=50,
    random_state=42
)

df = pd.concat(
    [df, duplicate_satirlar],
    ignore_index=True
)

df.to_csv(
    "gonderiler_faker.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Faker locale: tr_TR")
print("Seed: 42")
print("Toplam satir:", len(df))
print("Toplam sutun:", len(df.columns))
print("Duplicate:", df.duplicated().sum())
print("Eksik sehir:", df["alici_sehir"].isnull().sum())
print("Eksik agirlik:", df["agirlik_kg"].isnull().sum())

print("\nDosya olusturuldu: gonderiler_faker.csv")