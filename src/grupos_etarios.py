import pandas as pd


def obtener_promedio_grupos_etarios():
    archivo = "data/desempleo.xlsx"

    df = pd.read_excel(
        archivo,
        sheet_name="C1 total ",
        header=None
    )

    trimestres = df.iloc[4, 1:]

    # En Excel es fila 62, en Python es índice 61
    fila_inicio = 61

    grupos = df.iloc[fila_inicio + 1:fila_inicio + 6, 0]
    valores = df.iloc[fila_inicio + 1:fila_inicio + 6, 1:]

    datos_grupos = []

    for i, grupo in enumerate(grupos):
        datos = pd.DataFrame({
            "Trimestre": trimestres.values,
            "Grupo_etario": grupo,
            "Desempleados": valores.iloc[i].values
        })

        datos_grupos.append(datos)

    resultado = pd.concat(datos_grupos)
    resultado = resultado.dropna()

    resultado["Anio"] = resultado["Trimestre"].astype(str).str[-4:]

    resultado_actual = resultado[
        resultado["Anio"].isin(["2024", "2025"])
    ]
    promedio = (
        resultado_actual
        .groupby("Grupo_etario")["Desempleados"]
        .mean()
        .reset_index()
    )

    promedio = promedio.sort_values(
        by="Desempleados",
        ascending=False
    )

    return promedio