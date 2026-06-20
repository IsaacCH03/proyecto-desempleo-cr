import pandas as pd
import pulp
from src.grupos_etarios import obtener_promedio_grupos_etarios


def ejecutar_programacion_lineal():
    promedio_grupos = obtener_promedio_grupos_etarios()

    grupos = [
        "De 15 a 24 años",
        "De 25 a 34 años",
        "De 35 a 44 años",
        "De 45 a 59 años"
    ]

    promedio_grupos = promedio_grupos[
        promedio_grupos["Grupo_etario"].isin(grupos)
    ]

    desempleados = dict(
        zip(
            promedio_grupos["Grupo_etario"],
            promedio_grupos["Desempleados"]
        )
    )

    costos = {
        "De 15 a 24 años": 100000,
        "De 25 a 34 años": 120000,
        "De 35 a 44 años": 150000,
        "De 45 a 59 años": 160000
    }

    prioridad = {
        "De 15 a 24 años": 10,
        "De 25 a 34 años": 9,
        "De 35 a 44 años": 6,
        "De 45 a 59 años": 6
    }

    presupuesto = 500_000_000
    atencion_minima = 500

    modelo = pulp.LpProblem(
        "Optimizacion_de_recursos_para_atender_desempleo",
        pulp.LpMaximize
    )

    variables = {
        grupo: pulp.LpVariable(
            name=f"x_{grupo.replace(' ', '_')}",
            lowBound=0,
            cat="Integer"
        )
        for grupo in grupos
    }

    modelo += pulp.lpSum(
        prioridad[grupo] * variables[grupo]
        for grupo in grupos
    )

    modelo += pulp.lpSum(
        costos[grupo] * variables[grupo]
        for grupo in grupos
    ) <= presupuesto

    for grupo in grupos:
        modelo += variables[grupo] <= desempleados[grupo]
        modelo += variables[grupo] >= atencion_minima

    modelo.solve(pulp.PULP_CBC_CMD(msg=False))

    resultados = []

    for grupo in grupos:
        personas = variables[grupo].value()
        costo_total = personas * costos[grupo]
        impacto = personas * prioridad[grupo]
        desempleados_grupo = desempleados[grupo]

        resultados.append({
            "Grupo etario": grupo,
            "Personas beneficiadas": int(personas),
            "Desempleados promedio (INEC)": round(desempleados_grupo, 0),
            "Costo por persona": costos[grupo],
            "Costo total": int(costo_total),
            "% del presupuesto": round((costo_total / presupuesto) * 100, 2),
            "Prioridad": prioridad[grupo],
            "Impacto generado": int(impacto),
            "% de cobertura": round((personas / desempleados_grupo) * 100, 2)
        })

    resultado_df = pd.DataFrame(resultados)

    costo_total = resultado_df["Costo total"].sum()
    impacto_total = resultado_df["Impacto generado"].sum()

    return resultado_df, costo_total, impacto_total