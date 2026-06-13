import pandas as pd
import matplotlib.pyplot as plt


def graficar_desempleo_anual(datos):

    datos["Anio"] = datos["Trimestre"].str[-4:]

    promedio_anual = (
        datos.groupby("Anio")["Poblacion_desempleada"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(12,6))

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

    plt.savefig("graficos/desempleo_anual.png")

    plt.show()

    return promedio_anual