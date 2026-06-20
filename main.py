from src.cargar_datos import cargar_poblacion_desempleada
from src.analisis_actual import graficar_desempleo_anual
from src.pronosticos import generar_pronostico
from src.simulacion import simular_escenarios


def main():
    datos = cargar_poblacion_desempleada()

    print("\nDATOS INICIALES")
    print(datos.head())

    print("\nDATOS FINALES")
    print(datos.tail())

    print("\nPROMEDIO ANUAL")
    promedio_anual = graficar_desempleo_anual(datos)
    print(promedio_anual)

    print("\nPRONOSTICO")
    pronostico = generar_pronostico(datos)
    print(pronostico)

    print("\nSIMULACION")
    simulacion = simular_escenarios(datos)
    print(simulacion.to_string(index=False))


if __name__ == "__main__":
    main()