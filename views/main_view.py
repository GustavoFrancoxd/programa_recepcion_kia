import tkinter as tk
from tkinter import ttk
from views.components.reloj import Reloj
from views.components.tabla_citas import TablaCitas


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.fullscreen = False

        # Configurar ventana
        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        self.root.title("Citas para Área de Ventas")
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())

        # Configurar grid para expansión
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _crear_widgets(self):
        # Frame principal usando grid
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame principal
        self.main_frame.grid_rowconfigure(1, weight=1)  # Para la tabla
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Título (fila 0)
        self.titulo = tk.Label(
            self.main_frame,
            text="Citas para Área de Ventas",
            font=('Helvetica', 18, 'bold')
        )
        self.titulo.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # Reloj (fila 1)
        self.reloj = Reloj(self.main_frame)
        self.reloj.frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")

        # Frame contenedor para tabla (fila 2)
        self.tabla_container = tk.Frame(self.main_frame)
        self.tabla_container.grid(row=2, column=0, sticky="nsew")

        # Configurar expansión del contenedor de tabla
        self.tabla_container.grid_rowconfigure(0, weight=1)
        self.tabla_container.grid_columnconfigure(0, weight=1)

        # Tabla de citas
        self.tabla_citas = TablaCitas(self.tabla_container)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

        # Actualizar estilos
        self.tabla_citas.actualizar_estilo(self.fullscreen)
        font_size = 24 if self.fullscreen else 18
        self.titulo.config(font=('Helvetica', font_size, 'bold'))

    def mostrar_datos(self, datos):
        self.tabla_citas.actualizar_datos(datos)