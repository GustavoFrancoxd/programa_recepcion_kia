# main_view.py
import tkinter as tk
from views.components.reloj import Reloj
from views.components.tabla_citas import TablaCitas


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.fullscreen = True

        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        self.root.title("Citas para Área de Ventas")
        self.root.attributes('-fullscreen', self.fullscreen)
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _crear_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header_frame = tk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        self.titulo = tk.Label(
            header_frame,
            text="Citas para Área de Ventas",
            font=('Helvetica', 24, 'bold')
        )
        self.titulo.pack(side=tk.LEFT)

        self.reloj = Reloj(header_frame)
        self.reloj.frame.pack(side=tk.RIGHT)

        self.tabla_container = tk.Frame(self.main_frame)
        self.tabla_container.grid(row=2, column=0, sticky="nsew")

        self.tabla_container.grid_rowconfigure(0, weight=1)
        self.tabla_container.grid_columnconfigure(0, weight=1)

        self.tabla_citas = TablaCitas(self.tabla_container)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        self.tabla_citas._ajustar_filas()

    def mostrar_datos(self, datos):
        self.tabla_citas.actualizar_datos(datos)