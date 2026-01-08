from src.loader import load_consumption_csv
from src.validators import validate_15min_intervals


def run_engine():
    print("⚙️ CFE GDMTH Engine iniciado")

    df = load_consumption_csv("data/datos-consumo-electrico-01_15min.csv")

    validate_15min_intervals(df, "datetime")

    print("🚀 Dataset listo para clasificación tarifaria")
