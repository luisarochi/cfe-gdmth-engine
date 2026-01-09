import pandas as pd


def load_consumption_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Renombrar columnas al esquema interno del motor
    df.columns = ["datetime", "kWh"]

    # Parsear datetime
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)

    # Ordenar por tiempo
    df = df.sort_values("datetime")

    # Manejo de valores nulos de consumo
    null_count = df["kWh"].isnull().sum()
    if null_count > 0:
        print(
            f"⚠️ {null_count} intervalos con consumo nulo detectados. "
            "Se asumen como 0 kWh."
        )
        df["kWh"] = df["kWh"].fillna(0)

    return df
