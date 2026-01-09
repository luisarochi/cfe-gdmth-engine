import pandas as pd


def aggregate_monthly_energy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega consumo mensual total y por periodo tarifario.
    Retorna un DataFrame con:
    - month (YYYY-MM)
    - period (base/intermedia/punta)
    - kWh
    """

    df = df.copy()

    # Crear columna de mes
    df["month"] = df["datetime"].dt.to_period("M").astype(str)

    grouped = (
        df.groupby(["month", "period"], as_index=False)["kWh"]
        .sum()
    )

    return grouped


def aggregate_monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega consumo total mensual (todas las horas).
    """
    df = df.copy()
    df["month"] = df["datetime"].dt.to_period("M").astype(str)

    totals = (
        df.groupby("month", as_index=False)["kWh"]
        .sum()
        .rename(columns={"kWh": "total_kWh"})
    )

    return totals