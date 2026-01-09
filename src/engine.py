import json
import pandas as pd

from src.loader import load_consumption_csv
from src.validators import validate_15min_intervals
from src.period_resolver import resolve_gdmth_peninsular_period
from src.billing import calculate_gdmth_bill
from src.aggregations import (
    aggregate_monthly_energy,
    aggregate_monthly_totals,
)
from src.demand import (
    monthly_max_demand,
    monthly_max_demand_punta,
    demand_base_facturable
)



def run_engine():
    print("⚙️ CFE GDMTH Engine v1 - resolving periods")

    # =========================
    # 1️⃣ Cargar dataset
    # =========================
    df = load_consumption_csv("data/datos-consumo-electrico-01_15min.csv")

    # =========================
    # 2️⃣ Validaciones básicas
    # =========================
    validate_15min_intervals(df, "datetime")

    # =========================
    # 3️⃣ Resolver periodos GDMTH
    # =========================
    df = resolve_gdmth_peninsular_period(df, "datetime")

    # =====================
    # DEMANDA MEDIDA (kW)
    # =====================
    df["demand_kw"] = df["kWh"] * 4


    print("period")
    print(df["period"].value_counts())

    # =========================
    # 4️⃣ Columnas estructurales BASE
    # (estas NO deben vivir en agregations)
    # =========================
    df["month"] = df["datetime"].dt.to_period("M").astype(str)

    # =========================
    # 5️⃣ Agregaciones de energía
    # =========================
    monthly_period_kwh = aggregate_monthly_energy(df)
    monthly_total_kwh = aggregate_monthly_totals(df)


    # =========================
    # 6️⃣ Demanda máxima (15 min)
    # =========================
    max_demand = monthly_max_demand(df)
    max_demand_punta = monthly_max_demand_punta(df)
    base_facturable = demand_base_facturable(df)

    with open("config/gdmth_2024_peninsular.json") as f:
     tariffs = json.load(f)

    bill = calculate_gdmth_bill(
    energy_by_period=monthly_period_kwh,
    total_energy=monthly_total_kwh,
    demand_base=base_facturable,
    tariffs=tariffs
)
    print("\n📊 Consumo mensual por periodo:")
    print(monthly_period_kwh)

    monthly_period_kwh.to_csv(
    "outputs/monthly_energy_by_period.csv",
    index=False
)

    print("\n📊 Consumo mensual total:")
    print(monthly_total_kwh)

    monthly_total_kwh.to_csv(
    "outputs/monthly_totals.csv",
    index=False
)


    print("\n⚡ Demanda máxima mensual en punta (kW):")
    print(max_demand_punta)

    print("\n⚡ Demanda máxima mensual (kW):")
    print(max_demand)

    print("\n💵 Factura mensual estimada CFE GDMTH:")
    print(bill)

    bill.to_csv(
    "outputs/monthly_invoice.csv",
    index=False
)


    print("\n🏭 Demanda base facturable (kW):")
    print(base_facturable)


if __name__ == "__main__":
    run_engine()
