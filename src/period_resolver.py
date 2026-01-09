import pandas as pd


def resolve_gdmth_peninsular_period(df, datetime_col="datetime"):
    """
    Asigna periodo tarifario (base / intermedia / punta)
    para región Peninsular bajo esquema GDMTH.
    """
    def resolve_period(dt):
        hour = dt.hour
        weekday = dt.weekday()  # 0=lunes, 6=domingo
        month = dt.month

        # Temporada invierno: nov–mar (simplificado para v1)
        is_winter = month in [11, 12, 1, 2, 3]

        # Domingo
        if weekday == 6:
            return "base" if hour < 18 else "intermedia"

        # Lunes a viernes
        if weekday < 5:
            if is_winter:
                if 0 <= hour < 6 or hour >= 22:
                    return "base"
                elif 6 <= hour < 18:
                    return "intermedia"
                else:
                    return "punta"
            else:
                if 0 <= hour < 6 or hour >= 22:
                    return "base"
                elif 6 <= hour < 20:
                    return "intermedia"
                else:
                    return "punta"

        # Sábado
        if is_winter:
            if 0 <= hour < 8 or hour >= 21:
                return "base"
            elif 8 <= hour < 19:
                return "intermedia"
            else:
                return "punta"
        else:
            if 0 <= hour < 7:
                return "base"
            else:
                return "intermedia"

    df["period"] = df[datetime_col].apply(resolve_period)
    return df