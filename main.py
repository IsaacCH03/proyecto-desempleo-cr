import pandas as pd
from src.controller import ejecutar_metodo


# Evita que pandas trunque columnas con "..." al imprimir en consola
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.colheader_justify", "center")


def mostrar_menu():
    print("\n===== PROYECTO DE DESEMPLEO CR =====")
    print("1. Método de asignación")
    print("2. Programación lineal")
    print("0. Salir")


def formatear_resultado_pl(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea una copia del resultado de programación lineal con los montos
    y porcentajes formateados, únicamente para mostrarlo en consola.
    Los cálculos internos del modelo usan siempre los valores numéricos
    originales (esta función no los modifica).
    """
    df_mostrar = df.copy()

    df_mostrar["Desempleados promedio (INEC)"] = df_mostrar[
        "Desempleados promedio (INEC)"
    ].map("{:,.0f}".format)

    df_mostrar["Costo por persona"] = df_mostrar["Costo por persona"].map(
        "₡{:,.0f}".format
    )
    df_mostrar["Costo total"] = df_mostrar["Costo total"].map(
        "₡{:,.0f}".format
    )
    df_mostrar["% del presupuesto"] = df_mostrar["% del presupuesto"].map(
        "{:.2f}%".format
    )
    df_mostrar["% de cobertura"] = df_mostrar["% de cobertura"].map(
        "{:.2f}%".format
    )

    return df_mostrar


def main():
    while True:
        mostrar_menu()

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 0:
                print("\nPrograma finalizado.")
                break

            respuesta = ejecutar_metodo(opcion)

            print(f"\nMétodo ejecutado: {respuesta['metodo']}")

            if opcion == 2:
                print("\nResultados:")
                print(formatear_resultado_pl(respuesta["resultado"]))

                print("\nCosto total utilizado:")
                print(f"₡{respuesta['costo_total']:,.0f}")

                print("\nImpacto total generado:")
                print(respuesta["impacto_total"])

            else:
                print("\nResultados:")
                print(respuesta["resultado"])

                if opcion == 1:
                    print("\nBeneficio total ponderado:")
                    print(respuesta["beneficio_total"])

        except ValueError as error:
            print(f"\nError: {error}")

        except Exception as error:
            print(f"\nOcurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()
