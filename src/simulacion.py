import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simular_escenarios(datos, numero_simulaciones=10000, periodos_futuros=12):
    datos = datos.copy()

    datos["Poblacion_desempleada"] = datos["Poblacion_desempleada"].astype(float)
    datos["Anio"] = datos["Trimestre"].str[-4:].astype(int)

    datos_recientes = datos[datos["Anio"] >= 2024]

    variaciones = datos_recientes["Poblacion_desempleada"].diff().dropna()

    media_variacion = variaciones.mean()
    desviacion_variacion = variaciones.std()

    ultimo_valor = datos["Poblacion_desempleada"].iloc[-1]

    np.random.seed(7200)

    cambios_simulados = np.random.normal(
        media_variacion,
        desviacion_variacion,
        size=(numero_simulaciones, periodos_futuros)
    )

    valores_tendenciales = ultimo_valor + cambios_simulados.cumsum(axis=1)

    escenarios = {
        "Tendencial": 1.00,
        "Mejora moderada (-5%)": 0.95,
        "Mejora intensiva (-10%)": 0.90,
        "Deterioro (+5%)": 1.05
    }

    resultados = []

    for nombre, factor in escenarios.items():
        valores = valores_tendenciales * factor
        valor_final = valores[:, -1]
        promedio_periodos = valores.mean(axis=1)

        resultados.append({
            "Escenario": nombre,
            "Promedio_12_periodos": round(promedio_periodos.mean()),
            "Valor_final_esperado": round(valor_final.mean()),
            "Percentil_5_final": round(np.percentile(valor_final, 5)),
            "Percentil_95_final": round(np.percentile(valor_final, 95))
        })

    tabla_resultados = pd.DataFrame(resultados)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        tabla_resultados["Escenario"],
        tabla_resultados["Valor_final_esperado"]
    )

    ax.set_title("Comparacion de escenarios simulados")
    ax.set_ylabel("Personas desempleadas")
    ax.tick_params(axis="x", rotation=20)

    for i, valor in enumerate(tabla_resultados["Valor_final_esperado"]):
        ax.text(i, valor + 1000, f"{valor:,}", ha="center")

    fig.tight_layout()

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_grafico = os.path.join(base, "graficos", "simulacion_escenarios.png")
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)

    fig.savefig(ruta_grafico)

    return tabla_resultados, fig
