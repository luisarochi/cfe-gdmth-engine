# CFE GDMTH Energy Calculation Engine (v1)

Motor local de cálculo energético para estimar facturación CFE bajo esquema **GDMTH**,
a partir de perfiles de consumo eléctrico con granularidad de 15 minutos.

## Alcance v1
- Ejecución 100% local
- Cálculo mensual
- Tarifa: GDMTH
- Región inicial: Cancún (Peninsular)
- Periodos tarifarios: base, intermedia, punta
- Cargos soportados:
  - Energía
  - Demanda
  - Cargo fijo mínimo

## Inputs
Perfil de consumo eléctrico en intervalos de 15 minutos (kWh),
con timestamp en UTC, que será convertido a hora local para cálculo tarifario.

## Outputs
Desglose mensual de costos:
- Costo total
- Costo por energía
- Costo por demanda
- Cargo fijo
- Breakdown por periodo tarifario

## Supuestos
- El consumo está expresado en kWh por intervalo
- No se consideran subsidios ni impuestos adicionales
- Las reglas tarifarias se basan en normativa CFE vigente
- El depósito de garantía no se incluye en la factura mensual

## Roadmap
- v1: GDMTH, Cancún
- v2: más regiones y tarifas
- v3: API / servicio

## Ejecución
```bash
python main.py