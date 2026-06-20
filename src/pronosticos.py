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

    plt.figure(figsize=(12, 6))
    plt.plot(datos["Tiempo"], datos["Poblacion_desempleada"], label="Datos historicos")
    plt.plot(datos["Tiempo"], datos["Pronostico_ajustado"], label="Tendencia ajustada")
    plt.plot(x_futuro, pronostico["Pronostico_desempleo"], marker="o", label="Pronostico")

    plt.title("Pronostico de poblacion desempleada en Costa Rica")
    plt.xlabel("Periodos")
    plt.ylabel("Personas desempleadas")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficos/pronostico_desempleo.png")
    plt.show()

    return pronostico