import pandas as pd
from scipy.optimize import linear_sum_assignment
from src.grupos_etarios import obtener_promedio_grupos_etarios

def ejecutar_modelo_asignacion_corregido():
    programas = [
        "Capacitación técnica",
        "Emprendimiento",
        "Ferias de empleo",
        "Reconversión laboral"
    ]

    grupos = [
        "De 15 a 24 años",
        "De 25 a 34 años",
        "De 35 a 44 años",
        "De 45 a 59 años"
    ]

    # Matriz de impacto cualitativa/técnica base
    matriz_impacto = pd.DataFrame(
        [
            [95, 85, 60, 40],
            [75, 95, 80, 50],
            [85, 80, 70, 60],
            [40, 55, 85, 95]
        ],
        index=programas,
        columns=grupos
    )

    # Obtener los datos reales del INEC
    promedio_grupos = obtener_promedio_grupos_etarios()
    promedio_grupos = promedio_grupos[promedio_grupos["Grupo_etario"].isin(grupos)]
    
    desempleados_por_grupo = dict(
        zip(promedio_grupos["Grupo_etario"], promedio_grupos["Desempleados"])
    )

    matriz_para_optimizar = matriz_impacto * -1

    filas, columnas = linear_sum_assignment(matriz_para_optimizar)

    asignaciones = []
    for fila, columna in zip(filas, columnas):
        programa = programas[fila]
        grupo = grupos[columna]
        
        impacto_base = matriz_impacto.loc[programa, grupo]
        volumen_desempleados = desempleados_por_grupo.get(grupo, 0)
        
        # El beneficio real ponderado se calcula POST-optimización para la métrica final
        beneficio_real = (impacto_base / 100) * volumen_desempleados

        asignaciones.append({
            "Programa": programa,
            "Grupo asignado": grupo,
            "Impacto base (%)": impacto_base,
            "Promedio desempleados (INEC)": volumen_desempleados,
            "Impacto Social Estimado": beneficio_real
        })

    resultado = pd.DataFrame(asignaciones)
    impacto_total_sistema = resultado["Impacto Social Estimado"].sum()

    return resultado, impacto_total_sistema