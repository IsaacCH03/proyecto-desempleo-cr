import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configuración de estilo formal
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"

# Datos extraídos de tu consola
grupos = [
    "De 15 a 24 años\n(Capacitación)",
    "De 25 a 34 años\n(Emprendimiento)",
    "De 35 a 44 años\n(Ferias de Empleo)",
    "De 45 a 59 años\n(Reconversión)",
]

# Población original vs Población impactada (valores reales divididos entre 100)
desempleados_inec = [55835, 49795, 27130, 27504]
impacto_real = [53043, 47305, 18991, 26129]

x = np.arange(len(grupos))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

# Crear las barras
rects1 = ax.bar(
    x - width / 2,
    desempleados_inec,
    width,
    label="Población Desempleada (INEC)",
    color="#4A90E2",
)
rects2 = ax.bar(
    x + width / 2,
    impacto_real,
    width,
    label="Población Impactada Eficientemente",
    color="#2ECC71",
)

# Títulos y etiquetas formales
ax.set_ylabel("Número de Personas", fontsize=12, fontweight="bold")
ax.set_title(
    "Evaluación del Impacto Social: Población Desempleada vs. Asignación Óptima",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
ax.set_xticks(x)
ax.set_xticklabels(grupos, fontsize=10, fontweight="bold")
ax.legend(fontsize=11, loc="upper right")


# Función para añadir las etiquetas de datos sobre las barras
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{int(height):,}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 puntos de desfase vertical
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


autolabel(rects1)
autolabel(rects2)

# Ajustar el diseño para que no se corte nada
plt.tight_layout()
plt.savefig("impacto_social_desempleo.png", dpi=300)
plt.show()