import tkinter as tk
from tkinter import ttk

class TablaCitas:
    def __init__(self, parent):
        self.parent = parent
        self.datos_completos = []
        self.pagina_actual = 0
        self._crear_tabla()
        self.iniciar_paginacion()

    def _crear_tabla(self):
        columns = ('Cliente', 'Fecha', 'Hora', 'Asesor')
        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show='headings',
            height=5  # Mostrar solo 5 filas
        )

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def actualizar_datos(self, datos):
        """Actualiza los datos mostrados usando el caché"""
        self.datos_completos = datos
        self.pagina_actual = 0
        self.mostrar_pagina()

        # Reiniciar paginación solo si hay suficientes datos
        if len(self.datos_completos) > 5:
            if hasattr(self, 'timer_paginacion'):
                self.parent.after_cancel(self.timer_paginacion)
            self.iniciar_paginacion()

    def mostrar_pagina(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Calcular índices de la página actual
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        datos_pagina = self.datos_completos[inicio:fin]

        # Añadir datos de la página actual
        for dato in datos_pagina:
            self.tree.insert('', tk.END, values=(
                dato['cliente'],
                dato['fecha'],
                dato['hora'],
                dato['asesor']
            ))

    def siguiente_pagina(self):
        total_paginas = (len(self.datos_completos) + 4) // 5  # Redondeo hacia arriba
        self.pagina_actual = (self.pagina_actual + 1) % total_paginas
        self.mostrar_pagina()

    def iniciar_paginacion(self):
        self.timer_paginacion = self.parent.after(15000, self.ciclo_paginacion)

    def ciclo_paginacion(self):
        if len(self.datos_completos) > 5:
            self.siguiente_pagina()
        self.timer_paginacion = self.parent.after(15000, self.ciclo_paginacion)

    def detener_paginacion(self):
        if hasattr(self, 'timer_paginacion'):
            self.parent.after_cancel(self.timer_paginacion)