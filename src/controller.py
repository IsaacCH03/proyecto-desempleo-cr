from src.asignacion import ejecutar_modelo_asignacion_corregido  # Cambiado si renombraste la función
from src.programacion_lineal import ejecutar_programacion_lineal


def ejecutar_metodo(opcion: int):
    """
    Ejecuta el método seleccionado por el usuario.
    """

    if opcion == 1:
        # CAMBIO AQUÍ: Ahora capturamos solo las 2 variables que devuelve el nuevo modelo
        resultado, impacto_total_sistema = ejecutar_modelo_asignacion_corregido()

        # Adaptamos el diccionario de retorno para que la interfaz o el main no se rompan
        return {
            "metodo": "Asignación",
            "resultado": resultado,
            "beneficio_total": impacto_total_sistema,
            # Si el script principal necesita "promedio_grupos", puedes extraerlo directamente del dataframe de resultado
            "promedio_grupos": resultado[["Grupo asignado", "Promedio desempleados (INEC)"]]
        }

    elif opcion == 2:
        resultado, costo_total, impacto_total = (
            ejecutar_programacion_lineal()
        )

        return {
            "metodo": "Programación lineal",
            "resultado": resultado,
            "costo_total": costo_total,
            "impacto_total": impacto_total
        }

    else:
        raise ValueError("Opción no válida.")