import pandas as pd

from src.controller import ejecutar_metodo
from src.cargar_datos import cargar_poblacion_desempleada
from src.analisis_actual import graficar_desempleo_anual
from src.pronosticos import generar_pronostico
from src.simulacion import simular_escenarios

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.colheader_justify", "center")

def mostrar_menu():
print("\n===== PROYECTO DE DESEMPLEO CR =====")
print("1. Método de asignación")
print("2. Programación lineal")
print("3. Pronósticos + simulación")
print("0. Salir")

def formatear_resultado_pl(df: pd.DataFrame) -> pd.DataFrame:
df_mostrar = df.copy()

```
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
```

def ejecutar_pronosticos():
datos = cargar_poblacion_desempleada()

```
print("\nDATOS INICIALES")
print(datos.head())

print("\nDATOS FINALES")
print(datos.tail())

print("\nPROMEDIO ANUAL")
print(graficar_desempleo_anual(datos))

print("\nPRONOSTICO")
print(generar_pronostico(datos))

print("\nSIMULACION")
print(simular_escenarios(datos).to_string(index=False))
```

def main():
while True:
mostrar_menu()

```
    try:
        opcion = int(input("\nSeleccione una opción: "))

        if opcion == 0:
            print("\nPrograma finalizado.")
            break

        elif opcion == 3:
            ejecutar_pronosticos()

        else:
            respuesta = ejecutar_metodo(opcion)

            print(f"\nMétodo ejecutado: {respuesta['metodo']}")

            if opcion == 2:
                print(formatear_resultado_pl(respuesta["resultado"]))
                print(f"\nCosto total utilizado: ₡{respuesta['costo_total']:,.0f}")
                print(f"\nImpacto total generado: {respuesta['impacto_total']}")

            else:
                print(respuesta["resultado"])

                if opcion == 1:
                    print(
                        f"\nBeneficio total ponderado: "
                        f"{respuesta['beneficio_total']}"
                    )

    except ValueError as error:
        print(f"\nError: {error}")

    except Exception as error:
        print(f"\nOcurrió un error inesperado: {error}")
```

if **name** == "**main**":
main()
