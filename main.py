import pandas as pd

from src.controller import (
    ejecutar_metodo,
    formatear_resultado_pl,
)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.colheader_justify", "center")


def mostrar_menu():
    print("\n===== PROYECTO DE DESEMPLEO CR =====")
    print("1. Método de asignación")
    print("2. Programación lineal")
    print("3. Promedio anual de desempleo")
    print("4. Pronósticos")
    print("5. Simulación de escenarios")
    print("0. Salir")


def main():
    while True:
        mostrar_menu()

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 0:
                print("\nPrograma finalizado.")
                break

            else:
                respuesta = ejecutar_metodo(opcion)

                print(f"\nMétodo ejecutado: {respuesta['metodo']}")

                if opcion == 1:
                    print(respuesta["resultado"])
                    print(
                        f"\nBeneficio total ponderado: "
                        f"{respuesta['beneficio_total']}"
                    )

                elif opcion == 2:
                    print(formatear_resultado_pl(respuesta["resultado"]))
                    print(f"\nCosto total utilizado: ₡{respuesta['costo_total']:,.0f}")
                    print(f"\nImpacto total generado: {respuesta['impacto_total']}")

                elif opcion == 3:
                    print(respuesta["resultado"])
                    respuesta["figura"].show()

                elif opcion == 4:
                    print(respuesta["resultado"])
                    respuesta["figura"].show()

                elif opcion == 5:
                    print(respuesta["resultado"].to_string(index=False))
                    respuesta["figura"].show()

        except ValueError as error:
            print(f"\nError: {error}")

        except Exception as error:
            print(f"\nOcurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()
