import pandas as pd
import great_expectations as gx
import great_expectations.expectations as gxe

df = pd.read_csv(
    "gonderiler_temiz.csv",
    encoding="utf-8-sig"
)

context = gx.get_context(mode="ephemeral")

data_source = context.data_sources.add_pandas(
    name="kargo_pandas"
)

data_asset = data_source.add_dataframe_asset(
    name="gonderiler_temiz"
)

batch_definition = data_asset.add_batch_definition_whole_dataframe(
    name="tum_veri"
)

batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

kontroller = [
    (
        "Satir sayisi 4903 olmali",
        gxe.ExpectTableRowCountToEqual(value=4903)
    ),
    (
        "gonderi_id bos olmamali",
        gxe.ExpectColumnValuesToNotBeNull(column="gonderi_id")
    ),
    (
        "sube_kodu bos olmamali",
        gxe.ExpectColumnValuesToNotBeNull(column="sube_kodu")
    ),
    (
        "alici_sehir bos olmamali",
        gxe.ExpectColumnValuesToNotBeNull(column="alici_sehir")
    ),
    (
        "agirlik_kg bos olmamali",
        gxe.ExpectColumnValuesToNotBeNull(column="agirlik_kg")
    ),
    (
        "agirlik_kg pozitif olmali",
        gxe.ExpectColumnValuesToBeBetween(
            column="agirlik_kg",
            min_value=0,
            strict_min=True
        )
    )
]

tum_kontroller_basarili = True

print("\n--- VERI KALITE SONUCLARI ---\n")

for aciklama, expectation in kontroller:
    sonuc = batch.validate(expectation)

    if sonuc.success:
        print("[PASS]", aciklama)
    else:
        print("[FAIL]", aciklama)
        tum_kontroller_basarili = False

if tum_kontroller_basarili:
    print("\nTum veri kalite kontrolleri basarili.")
else:
    print("\nVeri kalite problemi bulundu.")