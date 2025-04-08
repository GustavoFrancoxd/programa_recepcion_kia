import tkinter as tk
from datetime import datetime


class Reloj:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.label = tk.Label(
            self.frame,
            font=('Helvetica', 12),
            padx=10  # Espaciado para mejor visualización
        )
        self.label.pack(side=tk.RIGHT)  # Alineación a la derecha

        self.actualizar()

    def actualizar(self):
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.label.config(text=ahora)
        self.label.after(1000, self.actualizar)