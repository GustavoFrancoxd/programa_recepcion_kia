import tkinter as tk
from tkinter import ttk


class TablaCitas:
    def __init__(self, parent):
        self.parent = parent
        self._crear_tabla()

    def _crear_tabla(self):
        columns = ('Cliente', 'Fecha', 'Hora', 'Asesor')
        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show='headings',
            height=10
        )

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.parent,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscroll=self.scrollbar.set)

        # Posicionar elementos
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def actualizar_datos(self, datos):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Añadir nuevos datos
        for dato in datos:
            self.tree.insert('', tk.END, values=(
                dato['cliente'],
                dato['fecha'],
                dato['hora'],
                dato['asesor']
            ))