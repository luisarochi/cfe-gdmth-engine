import pandas as pd


def calculate_demand_kw(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la demanda (kW) a partir de intervalos de 15 minutos.
    """
    df = df.copy()
    df["demand_kw"] = df["kWh"] * 4
    return df


def monthly_max_demand(df):
    return (
        df.groupby("month")["demand_kw"]
        .max()
        .reset_index()
    )
 

def monthly_punta_max_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demanda máxima mensual SOLO en periodo punta
    """
    punta_df = df[df["period"] == "punta"]

    result = (
        punta_df.groupby("month")["demand_kw"]
        .max()
        .reset_index(name="max_demand_kw_punta")
    )

def monthly_max_demand_punta(df):
    """
    Demanda máxima mensual coincidente en periodo punta (kW).
    """
    if "period" not in df.columns:
        raise ValueError("❌ La columna 'period' no existe")

    if "demand_kw" not in df.columns:
        raise ValueError("❌ La columna 'demand_kw' no existe")

    punta = df[df["period"] == "punta"].copy()

    if punta.empty:
        raise ValueError("❌ No existen intervalos punta en el dataset")

    punta["month"] = punta["datetime"].dt.to_period("M").astype(str)

    result = (
        punta
        .groupby("month")["demand_kw"]
        .max()
        .reset_index()
    )

def rolling_12m_max_demand(df):
    """
    Máxima demanda móvil 12 meses (kW).
    """
    monthly = monthly_max_demand(df)

    monthly["month_dt"] = pd.to_datetime(monthly["month"])
    monthly = monthly.sort_values("month_dt")

    monthly["rolling_12m_max_kw"] = (
        monthly["demand_kw"]
        .rolling(window=12, min_periods=1)
        .max()
    )

    return monthly[["month", "rolling_12m_max_kw"]]


def demand_base_facturable(df):
    """
    Demanda base facturable CFE GDMTH.
    """
    monthly = monthly_max_demand(df)
    rolling = rolling_12m_max_demand(df)

    result = monthly.merge(rolling, on="month")

    result["base_facturable_kw"] = result[
        ["demand_kw", "rolling_12m_max_kw"]
    ].max(axis=1)

    return result[["month", "base_facturable_kw"]]

