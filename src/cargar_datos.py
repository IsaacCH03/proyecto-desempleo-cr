import os
import pandas as pd


def cargar_poblacion_desempleada():
    # Ruta relativa a la raíz del proyecto, independiente del directorio de trabajo
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo = os.path.join(base, "data", "desempleo.xlsx")

    df = pd.read_excel(
        archivo,
        sheet_name="C1 total ",
        header=None
    )

    trimestres = df.iloc[4, 1:]
    desempleo = df[df[0] == "Desempleada"].iloc[0, 1:]

    datos_limpios = pd.DataFrame({
        "Trimestre": trimestres.values,
        "Poblacion_desempleada": desempleo.values
    })

    datos_limpios = datos_limpios.dropna()

    return datos_limpios
