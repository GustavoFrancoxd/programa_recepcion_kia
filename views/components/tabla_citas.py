import tkinter as tk
from tkinter import ttk


class TablaCitas:
    def __init__(self, parent):
        self.parent = parent
        self.datos_completos = []
        self.pagina_actual = 0

        # Configurar altura de filas (en píxeles)
        self.altura_fila_normal = 60  # Aumenté a 60px para modo normal
        self.altura_fila_fullscreen = 80  # 80px para pantalla completa

        self._configurar_estilos()
        self._crear_tabla()
        self.iniciar_paginacion()

    def _configurar_estilos(self):
        self.style = ttk.Style()

        # Configuración para modo normal
        self.style.configure("Normal.Treeview",
                             font=('Helvetica', 14),
                             rowheight=self.altura_fila_normal)  # Altura modificada

        self.style.configure("Normal.Treeview.Heading",
                             font=('Helvetica', 16, 'bold'))

        # Configuración para pantalla completa
        self.style.configure("Fullscreen.Treeview",
                             font=('Helvetica', 18),
                             rowheight=self.altura_fila_fullscreen)  # Altura aumentada

        self.style.configure("Fullscreen.Treeview.Heading",
                             font=('Helvetica', 20, 'bold'))

    def _crear_tabla(self):
        columns = ('Cliente', 'Fecha', 'Hora', 'Asesor')
        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show='headings',
            height=5,  # Mostrar exactamente 5 filas
            style="Normal.Treeview"
        )

        # Configurar columnas para que ocupen espacio uniforme
        ancho_columna = 200  # Ancho base para columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho_columna, anchor=tk.CENTER, stretch=True)

        # Asegurar que la tabla ocupe todo el espacio
        self.tree.pack(fill=tk.BOTH, expand=True)

    def actualizar_estilo(self, fullscreen):
        """Cambia entre estilos normal y pantalla completa"""
        if fullscreen:
            self.tree.configure(style="Fullscreen.Treeview")
            # Ajustar altura de filas para pantalla completa
            self.style.configure("Fullscreen.Treeview",
                                 rowheight=self.altura_fila_fullscreen)
        else:
            self.tree.configure(style="Normal.Treeview")
            # Ajustar altura de filas para modo normal
            self.style.configure("Normal.Treeview",
                                 rowheight=self.altura_fila_normal)

    def actualizar_datos(self, datos):
        self.datos_completos = datos
        self.pagina_actual = 0
        self.mostrar_pagina()

        if len(self.datos_completos) > 5:
            if hasattr(self, 'timer_paginacion'):
                self.parent.after_cancel(self.timer_paginacion)
            self.iniciar_paginacion()

    def mostrar_pagina(self):
        # Limpiar tabla
        self.tree.delete(*self.tree.get_children())

        # Calcular índices de la página actual
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        datos_pagina = self.datos_completos[inicio:fin]

        # Añadir datos
        for dato in datos_pagina:
            self.tree.insert('', tk.END, values=(
                dato['cliente'],
                dato['fecha'],
                dato['hora'],
                dato['asesor']
            ))

        # Asegurar que siempre se muestren 5 filas
        filas_mostradas = len(datos_pagina)
        if filas_mostradas < 5:
            for _ in range(5 - filas_mostradas):
                self.tree.insert('', tk.END, values=('', '', '', ''))

    # Resto de métodos permanecen igual...
    def siguiente_pagina(self):
        total_paginas = (len(self.datos_completos) + 4) // 5
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