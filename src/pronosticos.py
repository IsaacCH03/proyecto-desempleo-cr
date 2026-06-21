import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generar_pronostico(datos, periodos_futuros=12):
    datos = datos.copy()

    datos["Poblacion_desempleada"] = datos["Poblacion_desempleada"].astype(float)
    datos["Tiempo"] = np.arange(len(datos))

    x = datos["Tiempo"].values
    y = datos["Poblacion_desempleada"].values

    pendiente, intercepto = np.polyfit(x, y, 1)

    datos["Pronostico_ajustado"] = pendiente * x + intercepto

    x_futuro = np.arange(len(datos), len(datos) + periodos_futuros)
    y_futuro = pendiente * x_futuro + intercepto

    pronostico = pd.DataFrame({
        "Periodo": [f"Futuro {i+1}" for i in range(periodos_futuros)],
        "Pronostico_desempleo": np.round(y_futuro).astype(int)
    })

    print("\nCoeficiente de pendiente:", round(pendiente, 2))
    print("Intercepto:", round(intercepto, 2))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(datos["Tiempo"], datos["Poblacion_desempleada"], label="Datos historicos")
    ax.plot(datos["Tiempo"], datos["Pronostico_ajustado"], label="Tendencia ajustada")
    ax.plot(x_futuro, pronostico["Pronostico_desempleo"], marker="o", label="Pronostico")

    ax.set_title("Pronostico de poblacion desempleada en Costa Rica")
    ax.set_xlabel("Periodos")
    ax.set_ylabel("Personas desempleadas")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_grafico = os.path.join(base, "graficos", "pronostico_desempleo.png")
    os.makedirs(os.path.dirname(ruta_grafico), exist_ok=True)

    fig.savefig(ruta_grafico)

    return pronostico, fig
