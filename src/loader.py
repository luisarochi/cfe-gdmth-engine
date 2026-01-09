import pandas as pd
import pytz

CANCUN_TZ = "America/Cancun"
EXPECTED_INTERVAL_MINUTES = 15


def load_consumption_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        header=None,
        names=["timestamp_utc", "kwh"]
    )

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)

    cancun_tz = pytz.timezone(CANCUN_TZ)
    df["timestamp_local"] = df["timestamp_utc"].dt.tz_convert(cancun_tz)

    # ==========================
    # 1️⃣ VALIDAR INTERVALOS (ANTES DE LIMPIAR)
    # ==========================
    df = df.sort_values("timestamp_utc")
    diffs = df["timestamp_utc"].diff().dropna()
    expected = pd.Timedelta(minutes=EXPECTED_INTERVAL_MINUTES)

    if not (diffs == expected).all():
        raise ValueError(
            "El CSV no contiene intervalos consistentes de 15 minutos"
        )

    # ==========================
    # 2️⃣ LIMPIEZA DE CONSUMO
    # ==========================
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")

    invalid_rows = df[df["kwh"].isnull()]
    if not invalid_rows.empty:
        print("⚠️ Filas con consumo inválido detectadas:")
        print(invalid_rows.head(10))
        print(f"⚠️ Total de filas inválidas: {len(invalid_rows)}")

    df = df.dropna(subset=["kwh"])

    if (df["kwh"] < 0).any():
        raise ValueError("El CSV contiene valores negativos de consumo")

    return df