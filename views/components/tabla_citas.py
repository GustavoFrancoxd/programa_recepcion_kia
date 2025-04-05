# tabla_citas.py
import tkinter as tk
from tkinter import ttk


class TablaCitas:
    def __init__(self, parent):
        self.parent = parent
        self.datos_completos = []
        self.pagina_actual = 0
        self.ELEMENTOS_POR_PAGINA = 7  # 7 elementos reales + 1 fila vacía
        self.TOTAL_FILAS = 8  # Filas a mostrar

        self.altura_base = 40
        self._configurar_estilos()
        self._crear_tabla()
        self.iniciar_paginacion()
        self.parent.bind("<Configure>", self._ajustar_filas)

    def _configurar_estilos(self):
        self.style = ttk.Style()
        self.style.configure("Dynamic.Treeview",
                             font=('Helvetica', 14),
                             rowheight=self.altura_base)
        self.style.configure("Dynamic.Treeview.Heading",
                             font=('Helvetica', 16, 'bold'))

    def _crear_tabla(self):
        columns = ('Cliente', 'Fecha', 'Hora', 'Asesor')
        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show='headings',
            style="Dynamic.Treeview",
            selectmode='none',
            height=self.TOTAL_FILAS  # Mostrar 8 filas siempre
        )

        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, stretch=True)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def _ajustar_filas(self, event=None):
        altura_contenedor = self.parent.winfo_height()
        if altura_contenedor > 0:
            nueva_altura = altura_contenedor // self.TOTAL_FILAS
            self.style.configure("Dynamic.Treeview", rowheight=nueva_altura)

            font_size = max(12, int(nueva_altura * 0.3))
            self.style.configure("Dynamic.Treeview", font=('Helvetica', font_size))
            self.style.configure("Dynamic.Treeview.Heading",
                                 font=('Helvetica', font_size + 2, 'bold'))

    def actualizar_datos(self, datos):
        self.datos_completos = datos
        self.pagina_actual = 0
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.tree.delete(*self.tree.get_children())

        inicio = self.pagina_actual * self.ELEMENTOS_POR_PAGINA
        fin = inicio + self.ELEMENTOS_POR_PAGINA
        datos_pagina = self.datos_completos[inicio:fin]

        # Insertar máximo 7 elementos reales
        for dato in datos_pagina:
            self.tree.insert('', tk.END, values=(
                dato['cliente'],
                dato['fecha'],
                dato['hora'],
                dato['asesor']
            ))

        # Añadir filas vacías para completar 8
        total_filas_vacias = self.TOTAL_FILAS - len(datos_pagina)
        for _ in range(total_filas_vacias):
            self.tree.insert('', tk.END, values=('', '', '', ''))

    def siguiente_pagina(self):
        total_paginas = max(1, (len(self.datos_completos) + self.ELEMENTOS_POR_PAGINA - 1) // self.ELEMENTOS_POR_PAGINA)
        self.pagina_actual = (self.pagina_actual + 1) % total_paginas
        self.mostrar_pagina()

    def iniciar_paginacion(self):
        if hasattr(self, 'timer_paginacion'):
            self.parent.after_cancel(self.timer_paginacion)
        self.timer_paginacion = self.parent.after(15000, self.ciclo_paginacion)

    def ciclo_paginacion(self):
        if len(self.datos_completos) > self.ELEMENTOS_POR_PAGINA:
            self.siguiente_pagina()
        self.iniciar_paginacion()

    def detener_paginacion(self):
        if hasattr(self, 'timer_paginacion'):
            self.parent.after_cancel(self.timer_paginacion)