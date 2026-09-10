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

df.to_sql(
    "gonderiler",
    con=engine,
    if_exists="append",
    index=False
)

with engine.connect() as conn:
    toplam = conn.execute(
        text("SELECT COUNT(*) FROM gonderiler")
    ).scalar()

print("CSV satir sayisi:", len(df))
print("Veritabanindaki toplam satir:", toplam)