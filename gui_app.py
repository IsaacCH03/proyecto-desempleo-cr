import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.controller import ejecutar_metodo, formatear_resultado_pl


METODOS = {
    1: "Método de asignación",
    2: "Programación lineal",
    3: "Promedio anual de desempleo",
    4: "Pronósticos",
    5: "Simulación de escenarios",
}


class AppDesempleoCR(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Proyecto Desempleo CR")
        self.geometry("1300x760")
        self.minsize(950, 600)
        self.configure(bg="white")

        # Abrimos maximizada para aprovechar todo el ancho disponible
        # (la tabla de programación lineal tiene 9 columnas y necesita
        # espacio). Si el sistema no soporta 'zoomed' (algunos Linux),
        # caemos a pantalla completa con Escape para salir de ese modo.
        try:
            self.state("zoomed")
        except tk.TclError:
            try:
                self.attributes("-zoomed", True)
            except tk.TclError:
                pass

        # Guardamos la figura mostrada actualmente para poder cerrarla
        # con matplotlib (plt.close) cuando se cambia de método.
        self.figura_actual = None

        self._construir_layout()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _construir_layout(self):
        barra = tk.Frame(self, bg="#1f2937", width=250)
        barra.pack(side="left", fill="y")

        tk.Label(
            barra,
            text="Desempleo\nCosta Rica",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 16, "bold"),
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=18, pady=(25, 20))

        for opcion, nombre in METODOS.items():
            tk.Button(
                barra,
                text=f"{opcion}. {nombre}",
                anchor="w",
                bg="#374151",
                fg="white",
                activebackground="#4b5563",
                activeforeground="white",
                relief="flat",
                font=("Segoe UI", 10),
                padx=10,
                pady=12,
                cursor="hand2",
                command=lambda o=opcion: self.ejecutar(o),
            ).pack(fill="x", padx=18, pady=4)

        tk.Button(
            barra,
            text="Salir",
            bg="#7f1d1d",
            fg="white",
            activebackground="#991b1b",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=12,
            cursor="hand2",
            command=self.destroy,
        ).pack(fill="x", padx=18, pady=(40, 18))

        contenedor = tk.Frame(self, bg="white")
        contenedor.pack(side="right", fill="both", expand=True)

        self.titulo_metodo = tk.Label(
            contenedor,
            text="Seleccione un método en el menú",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            anchor="w",
            fg="#111827",
        )
        self.titulo_metodo.pack(fill="x", padx=25, pady=(20, 5))

        self.resumen_label = tk.Label(
            contenedor,
            text="",
            font=("Segoe UI", 11),
            bg="white",
            justify="left",
            anchor="w",
            fg="#1f2937",
            wraplength=820,
        )
        self.resumen_label.pack(fill="x", padx=25, pady=(0, 10))

        # Área con scroll donde se dibuja la tabla y/o la gráfica
        area_scroll = tk.Frame(contenedor, bg="white")
        area_scroll.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        self.canvas_contenido = tk.Canvas(area_scroll, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            area_scroll, orient="vertical", command=self.canvas_contenido.yview
        )

        self.frame_scrollable = tk.Frame(self.canvas_contenido, bg="white")
        self.frame_scrollable.bind(
            "<Configure>",
            lambda e: self.canvas_contenido.configure(
                scrollregion=self.canvas_contenido.bbox("all")
            ),
        )

        self.canvas_contenido.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas_contenido.configure(yscrollcommand=scrollbar.set)

        self.canvas_contenido.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ------------------------------------------------------------------
    # Lógica de ejecución de métodos
    # ------------------------------------------------------------------
    def _limpiar_contenido(self):
        for widget in self.frame_scrollable.winfo_children():
            widget.destroy()

        if self.figura_actual is not None:
            plt.close(self.figura_actual)
            self.figura_actual = None

    def ejecutar(self, opcion: int):
        self._limpiar_contenido()
        self.titulo_metodo.config(text="Calculando, un momento...")
        self.resumen_label.config(text="")
        self.update_idletasks()

        try:
            respuesta = ejecutar_metodo(opcion)
        except Exception as error:
            self.titulo_metodo.config(text="Ocurrió un error")
            messagebox.showerror(
                "Error al ejecutar el método",
                f"{error}",
            )
            return

        self.titulo_metodo.config(text=f"Método ejecutado: {respuesta['metodo']}")

        if opcion == 1:
            self._mostrar_tabla(respuesta["resultado"])
            self.resumen_label.config(
                text=(
                    "Beneficio total ponderado (Impacto Social Estimado): "
                    f"{respuesta['beneficio_total']:,.2f}"
                )
            )

        elif opcion == 2:
            df_formateado = formatear_resultado_pl(respuesta["resultado"])
            self._mostrar_tabla(df_formateado)
            self.resumen_label.config(
                text=(
                    f"Costo total utilizado: ₡{respuesta['costo_total']:,.0f}    |    "
                    f"Impacto total generado: {respuesta['impacto_total']:,}"
                )
            )

        elif opcion in (3, 4, 5):
            self._mostrar_tabla(respuesta["resultado"])
            self._mostrar_figura(respuesta["figura"])

    # ------------------------------------------------------------------
    # Helpers de presentación
    # ------------------------------------------------------------------
    def _mostrar_tabla(self, df):
        frame = tk.Frame(self.frame_scrollable, bg="white")
        frame.pack(fill="x", pady=(5, 15))

        columnas = list(df.columns)
        alto = max(1, min(len(df), 8))

        estilo = ttk.Style()
        estilo.configure("Tabla.Treeview", rowheight=26, font=("Segoe UI", 9))
        estilo.configure("Tabla.Treeview.Heading", font=("Segoe UI", 9, "bold"))

        tree = ttk.Treeview(
            frame, columns=columnas, show="headings", height=alto, style="Tabla.Treeview"
        )

        # Medimos el texto real (encabezado y celdas) para que cada columna
        # tenga solo el ancho que necesita, en vez de un ancho fijo igual
        # para todas. Así columnas cortas ("Prioridad") quedan angostas y
        # dejan espacio a las que sí necesitan más ("Desempleados promedio").
        fuente_celda = tkfont.Font(family="Segoe UI", size=9)
        fuente_encabezado = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        for col in columnas:
            valores_col = df[col].astype(str)
            ancho_contenido = max(
                (fuente_celda.measure(v) for v in valores_col), default=0
            )
            ancho_encabezado = fuente_encabezado.measure(str(col))
            ancho = max(ancho_contenido, ancho_encabezado) + 20
            ancho = max(65, min(ancho, 230))  # límites razonables

            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=ancho, stretch=False)

        for _, fila in df.iterrows():
            tree.insert("", "end", values=list(fila))

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)

    def _mostrar_figura(self, fig):
        self.figura_actual = fig

        canvas = FigureCanvasTkAgg(fig, master=self.frame_scrollable)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, pady=10)


if __name__ == "__main__":
    app = AppDesempleoCR()
    app.mainloop()