from src.cargar_datos import cargar_poblacion_desempleada
from src.analisis_actual import graficar_desempleo_anual

def main():

    datos = cargar_poblacion_desempleada()

    promedio_anual = graficar_desempleo_anual(datos)

    print(promedio_anual)

if __name__ == "__main__":
    main()