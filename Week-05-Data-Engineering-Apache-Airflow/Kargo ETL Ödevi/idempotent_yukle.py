import pandas as pd
from sqlalchemy import create_engine, text, inspect

df = pd.read_csv(
    "gonderiler_temiz.csv",
    encoding="utf-8-sig",
    parse_dates=["kabul_tarihi", "teslim_tarihi"]
)

engine = create_engine(
    "postgresql+psycopg2://kargo_user:kargo123@localhost:5432/kargo_db"
)

# Tablo yoksa once bos tabloyu olustur
inspector = inspect(engine)

if not inspector.has_table("gonderiler"):
    df.head(0).to_sql(
        "gonderiler",
        con=engine,
        if_exists="replace",
        index=False
    )

    with engine.begin() as conn:
        conn.execute(
            text("""
                ALTER TABLE gonderiler
                ADD PRIMARY KEY (gonderi_id)
            """)
        )

# NaN / NaT degerlerini Python None'a cevir
df = df.astype(object).where(pd.notnull(df), None)

kayitlar = df.to_dict(orient="records")

upsert_sql = text("""
    INSERT INTO gonderiler (
        gonderi_id,
        sube_kodu,
        alici_sehir,
        agirlik_kg,
        durum,
        kabul_tarihi,
        teslim_tarihi
    )
    VALUES (
        :gonderi_id,
        :sube_kodu,
        :alici_sehir,
        :agirlik_kg,
        :durum,
        :kabul_tarihi,
        :teslim_tarihi
    )
    ON CONFLICT (gonderi_id)
    DO UPDATE SET
        sube_kodu = EXCLUDED.sube_kodu,
        alici_sehir = EXCLUDED.alici_sehir,
        agirlik_kg = EXCLUDED.agirlik_kg,
        durum = EXCLUDED.durum,
        kabul_tarihi = EXCLUDED.kabul_tarihi,
        teslim_tarihi = EXCLUDED.teslim_tarihi
""")

with engine.begin() as conn:
    conn.execute(upsert_sql, kayitlar)

with engine.connect() as conn:
    toplam = conn.execute(
        text("SELECT COUNT(*) FROM gonderiler")
    ).scalar()

print("CSV satir sayisi:", len(df))
print("Veritabanindaki toplam satir:", toplam)
print("Idempotent yukleme tamamlandi.")