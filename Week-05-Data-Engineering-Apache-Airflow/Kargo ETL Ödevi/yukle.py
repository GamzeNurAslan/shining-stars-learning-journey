import pandas as pd
from sqlalchemy import create_engine, text

df = pd.read_csv(
    "gonderiler_temiz.csv",
    encoding="utf-8-sig",
    parse_dates=["kabul_tarihi", "teslim_tarihi"]
)

engine = create_engine(
    "postgresql+psycopg2://kargo_user:kargo123@localhost:5432/kargo_db"
)

print("CSV satir sayisi:", len(df))
print("Benzersiz gonderi_id:", df["gonderi_id"].nunique())

df.to_sql(
    "gonderiler",
    con=engine,
    if_exists="replace",
    index=False
)

with engine.connect() as conn:
    sonuc = conn.execute(
        text("SELECT COUNT(*) FROM gonderiler")
    ).scalar()

print("PostgreSQL satir sayisi:", sonuc)
print("Veri basariyla PostgreSQL'e yazildi.")