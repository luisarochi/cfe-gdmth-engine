from src.loader import load_consumption_csv
from src.validators import validate_15min_intervals
from src.period_resolver import resolve_gdmth_peninsular_period
from src.aggregations import (
    aggregate_monthly_energy,
    aggregate_monthly_totals,
)


def run_engine():
    print("⚙️ CFE GDMTH Engine v1 - resolving periods")

    df = load_consumption_csv("data/datos-consumo-electrico-01_15min.csv")

    validate_15min_intervals(df, "datetime")

    df["period"] = df["datetime"].apply(
        resolve_gdmth_peninsular_period
    )

    print("✅ Periodos tarifarios asignados")
    print(df["period"].value_counts())

    # 👇👇👇 AQUÍ VA LA AGREGACIÓN 👇👇👇
    energy_by_period = aggregate_monthly_energy(df)
    monthly_totals = aggregate_monthly_totals(df)

    print("\n📊 Consumo mensual por periodo:")
    print(energy_by_period)

    print("\n📊 Consumo mensual total:")
    print(monthly_totals)

    print("🚀 Dataset listo para cálculo energético")
