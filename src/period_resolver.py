from datetime import datetime, time

# Periodos Región Peninsular – GDMTH

SUMMER_PERIOD = {
    "weekday": {
        "base": [(time(0, 0), time(6, 0))],
        "intermedia": [(time(6, 0), time(20, 0))],
        "punta": [(time(20, 0), time(22, 0))],
        "base_2": [(time(22, 0), time(23, 59, 59))]
    },
    "saturday": {
        "base": [(time(0, 0), time(7, 0))],
        "intermedia": [(time(7, 0), time(23, 59, 59))]
    },
    "sunday": {
        "base": [(time(0, 0), time(19, 0))],
        "intermedia": [(time(19, 0), time(23, 59, 59))]
    }
}

WINTER_PERIOD = {
    "weekday": {
        "base": [(time(0, 0), time(6, 0))],
        "intermedia": [(time(6, 0), time(18, 0))],
        "punta": [(time(18, 0), time(22, 0))],
        "base_2": [(time(22, 0), time(23, 59, 59))]
    },
    "saturday": {
        "base": [(time(0, 0), time(8, 0))],
        "intermedia": [(time(8, 0), time(19, 0))],
        "punta": [(time(19, 0), time(21, 0))],
        "base_2": [(time(21, 0), time(23, 59, 59))]
    },
    "sunday": {
        "base": [(time(0, 0), time(18, 0))],
        "intermedia": [(time(18, 0), time(23, 59, 59))]
    }
}


def resolve_day_type(ts: datetime) -> str:
    if ts.weekday() < 5:
        return "weekday"
    elif ts.weekday() == 5:
        return "saturday"
    else:
        return "sunday"


def resolve_season(ts: datetime) -> str:
    """
    Simplificación v1:
    Abril–Octubre = verano
    Noviembre–Marzo = invierno
    """
    if 4 <= ts.month <= 10:
        return "summer"
    return "winter"


def resolve_period(ts: datetime) -> str:
    day_type = resolve_day_type(ts)
    season = resolve_season(ts)

    periods = SUMMER_PERIOD if season == "summer" else WINTER_PERIOD
    rules = periods[day_type]

    current_time = ts.time()

    for period, ranges in rules.items():
        for start, end in ranges:
            if start <= current_time <= end:
                if period.startswith("base"):
                    return "base"
                return period

    raise ValueError(f"No se pudo resolver periodo tarifario para {ts}")