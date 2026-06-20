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

    plt.figure(figsize=(12, 6))

    plt.plot(
        promedio_anual["Anio"],
        promedio_anual["Poblacion_desempleada"],
        marker="o"
    )

    plt.title("Promedio anual de población desempleada en Costa Rica")
    plt.xlabel("Año")
    plt.ylabel("Personas desempleadas")
    plt.grid(True)
    plt.tight_layout()


    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_grafico = os.path.join(base, "graficos", "desempleo_anual.png")
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)

    plt.savefig(ruta_grafico)
    plt.show()

    return promedio_anual
