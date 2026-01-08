import pandas as pd
import pytz

CANCUN_TZ = "America/Cancun"


def load_consumption_csv(path: str) -> pd.DataFrame:
    """
    Carga un CSV de consumo eléctrico con intervalos de 15 minutos.
    El CSV no tiene headers y viene en formato:
    timestamp (UTC), kWh

    Retorna un DataFrame con:
    - timestamp_utc
    - timestamp_local
    - kwh
    """

    # Leer CSV sin header
    df = pd.read_csv(
        path,
        header=None,
        names=["timestamp_utc", "kwh"]
    )

    # Parsear timestamps como datetime UTC
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)

    # Convertir a hora local Cancún
    cancun_tz = pytz.timezone(CANCUN_TZ)
    df["timestamp_local"] = df["timestamp_utc"].dt.tz_convert(cancun_tz)

    # Validaciones básicas
    if df["kwh"].isnull().any():
        raise ValueError("El CSV contiene valores nulos de consumo")

    if (df["kwh"] < 0).any():
        raise ValueError("El CSV contiene valores negativos de consumo")

    return df