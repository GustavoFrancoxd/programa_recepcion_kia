import tkinter as tk
from datetime import datetime


class Reloj:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.grid(sticky="ew")  # Cambiado de pack() a grid()

        self.label = tk.Label(
            self.frame,
            font=('Helvetica', 12)
        )
        self.label.pack(anchor=tk.CENTER)  # Mantenemos pack() interno al frame

        self.actualizar()

    def actualizar(self):
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.label.config(text=ahora)
        self.label.after(1000, self.actualizar)