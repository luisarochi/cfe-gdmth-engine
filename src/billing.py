import pandas as pd


def calculate_gdmth_bill(
    energy_by_period: pd.DataFrame,
    total_energy: pd.DataFrame,
    demand_base: pd.DataFrame,
    tariffs: dict
):
    """
    Calcula factura mensual CFE GDMTH
    """

    # ─────────────────────────────
    # Energía por periodo
    # ─────────────────────────────
    energy_cost = energy_by_period.copy()
    energy_cost["energy_cost"] = energy_cost.apply(
        lambda r: r["kWh"] * tariffs["energy"][r["period"]],
        axis=1
    )

    energy_monthly = (
        energy_cost
        .groupby("month")[["energy_cost"]]
        .sum()
        .reset_index()
    )

    # ─────────────────────────────
    # Demanda
    # ─────────────────────────────
    demand_cost = demand_base.copy()
    demand_cost["demand_cost"] = (
        demand_cost["base_facturable_kw"] *
        tariffs["demand"]["base"]
    )

    # ─────────────────────────────
    # Merge final
    # ─────────────────────────────
    bill = (
        energy_monthly
        .merge(demand_cost, on="month")
        .merge(total_energy, on="month")
    )

    bill["total_bill"] = (
        bill["energy_cost"] +
        bill["demand_cost"]
    )

    return bill
