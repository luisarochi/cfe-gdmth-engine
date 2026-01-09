# Supuestos — CFE GDMTH Engine v1

Este motor calcula una estimación del costo de suministro eléctrico
bajo tarifa GDMTH utilizando perfiles de consumo cada 15 minutos.

## Supuestos principales

- La demanda se calcula como kWh × 4 para intervalos de 15 minutos.
- Valores nulos de consumo se asumen como 0 kWh.
- Se utilizan periodos tarifarios definidos por CFE para la región Peninsular.
- No se consideran penalizaciones por factor de potencia.
- No se consideran ajustes por redondeos comerciales de CFE.
- Las tarifas provienen de publicaciones oficiales de CFE.

## Alcance

- Motor local de cálculo
- Resultados reproducibles
- Uso analítico / comparativo

## No cubre

- Facturación oficial CFE
- Ajustes por medición física
- Cargos extraordinarios
