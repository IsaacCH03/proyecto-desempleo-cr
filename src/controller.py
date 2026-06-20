import pandas as pd

from src.asignacion import ejecutar_modelo_asignacion_corregido
from src.programacion_lineal import ejecutar_programacion_lineal
from src.cargar_datos import cargar_poblacion_desempleada
from src.analisis_actual import graficar_desempleo_anual
from src.pronosticos import generar_pronostico
from src.simulacion import simular_escenarios


def formatear_resultado_pl(df: pd.DataFrame) -> pd.DataFrame:
    df_mostrar = df.copy()

    df_mostrar["Desempleados promedio (INEC)"] = (
        df_mostrar["Desempleados promedio (INEC)"]
        .map("{:,.0f}".format)
    )

    df_mostrar["Costo por persona"] = (
        df_mostrar["Costo por persona"]
        .map("₡{:,.0f}".format)
    )

    df_mostrar["Costo total"] = (
        df_mostrar["Costo total"]
        .map("₡{:,.0f}".format)
    )

    df_mostrar["% del presupuesto"] = (
        df_mostrar["% del presupuesto"]
        .map("{:.2f}%".format)
    )

    df_mostrar["% de cobertura"] = (
        df_mostrar["% de cobertura"]
        .map("{:.2f}%".format)
    )

    return df_mostrar


def ejecutar_metodo(opcion: int) -> dict:
    """
    Ejecuta el método seleccionado por el usuario y devuelve un diccionario
    con los resultados listos para que main.py los imprima.
    """

    if opcion == 1:
        resultado, impacto_total_sistema = ejecutar_modelo_asignacion_corregido()

        return {
            "metodo": "Asignación",
            "resultado": resultado,
            "beneficio_total": impacto_total_sistema,
            "promedio_grupos": resultado[
                ["Grupo asignado", "Promedio desempleados (INEC)"]
            ],
        }

    elif opcion == 2:
        resultado, costo_total, impacto_total = ejecutar_programacion_lineal()

        return {
            "metodo": "Programación lineal",
            "resultado": resultado,
            "costo_total": costo_total,
            "impacto_total": impacto_total,
        }

    elif opcion == 3:
        datos = cargar_poblacion_desempleada()
        resultado = graficar_desempleo_anual(datos)

        return {
            "metodo": "Promedio anual de desempleo",
            "resultado": resultado,
        }

    elif opcion == 4:
        datos = cargar_poblacion_desempleada()

        print("\nDATOS INICIALES")
        print(datos.head())

        print("\nDATOS FINALES")
        print(datos.tail())

        resultado = generar_pronostico(datos)

        return {
            "metodo": "Pronósticos",
            "resultado": resultado,
        }

    elif opcion == 5:
        datos = cargar_poblacion_desempleada()
        resultado = simular_escenarios(datos)

        return {
            "metodo": "Simulación de escenarios",
            "resultado": resultado,
        }

    else:
        raise ValueError("Opción no válida. Seleccione entre 0 y 5.")
