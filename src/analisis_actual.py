import os
import pandas as pd
import matplotlib.pyplot as plt


def graficar_desempleo_anual(datos):
    datos = datos.copy()

    datos["Anio"] = datos["Trimestre"].str[-4:]

    promedio_anual = (
        datos.groupby("Anio")["Poblacion_desempleada"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        promedio_anual["Anio"],
        promedio_anual["Poblacion_desempleada"],
        marker="o"
    )

    ax.set_title("Promedio anual de población desempleada en Costa Rica")
    ax.set_xlabel("Año")
    ax.set_ylabel("Personas desempleadas")
    ax.grid(True)
    fig.tight_layout()

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_grafico = os.path.join(base, "graficos", "desempleo_anual.png")
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)

    fig.savefig(ruta_grafico)

    return promedio_anual, fig
