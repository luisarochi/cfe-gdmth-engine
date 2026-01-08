from datetime import datetime


def resolve_gdmth_peninsular_period(dt: datetime) -> str:
    """
    Clasifica un datetime en Base / Intermedia / Punta
    para tarifa GDMTH región Peninsular (invierno).
    """

    hour = dt.hour
    weekday = dt.weekday()  # 0=lunes, 6=domingo

    # Domingo
    if weekday == 6:
        if hour < 18:
            return "base"
        else:
            return "punta"

    # Sábado
    if weekday == 5:
        if hour < 8:
            return "base"
        elif hour < 19:
            return "intermedia"
        elif hour < 21:
            return "punta"
        else:
            return "intermedia"

    # Lunes a viernes
    if hour < 6:
        return "base"
    elif hour < 18:
        return "intermedia"
    elif hour < 22:
        return "punta"
    else:
        return "base"
