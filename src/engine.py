from src.loader import load_consumption_csv
from src.validators import validate_15min_intervals
from src.period_resolver import resolve_gdmth_peninsular_period


def run_engine():
    print("⚙️ CFE GDMTH Engine v1 - resolving periods")

    df = load_consumption_csv("data/datos-consumo-electrico-01_15min.csv")

    validate_15min_intervals(df, "datetime")

    # Resolver periodo tarifario
    df["period"] = df["datetime"].apply(
        resolve_gdmth_peninsular_period
    )

    print("✅ Periodos tarifarios asignados")
    print(df["period"].value_counts())

    print("🚀 Dataset listo para cálculo energético")
