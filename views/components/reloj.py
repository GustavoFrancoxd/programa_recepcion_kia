import tkinter as tk
from datetime import datetime


class Reloj:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(anchor=tk.NE)

        self.label = tk.Label(
            self.frame,
            font=('Helvetica', 10)
        )
        self.label.pack()

        self.actualizar()

    def actualizar(self):
        ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.label.config(text=ahora)
        self.label.after(1000, self.actualizar)