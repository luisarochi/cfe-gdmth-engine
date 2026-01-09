import pandas as pd


def validate_15min_intervals(df, datetime_col):
    """
    Valida que los registros estén espaciados cada 15 minutos.
    """
    df = df.sort_values(datetime_col)
    diffs = df[datetime_col].diff().dropna()

    invalid = diffs[diffs != pd.Timedelta(minutes=15)]

    if not invalid.empty:
        raise ValueError(
            f"❌ Intervalos inválidos detectados. "
            f"Ejemplo:\n{invalid.head()}"
        )

    print("✅ Intervalos de 15 minutos válidos")