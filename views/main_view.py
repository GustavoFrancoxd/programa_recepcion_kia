# main_view.py
import tkinter as tk
from views.components.reloj import Reloj
from views.components.tabla_citas import TablaCitas


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        self.root.title("Citas para Área de Ventas")
        self.root.geometry("1200x800")  # Tamaño inicial personalizado
        self.root.bind('<Configure>', self._ajustar_tabla)

    def _crear_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        self.titulo = tk.Label(
            header_frame,
            text="Citas para Área de Ventas",
            font=('Helvetica', 24, 'bold')
        )
        self.titulo.pack(side=tk.LEFT)

        self.reloj = Reloj(header_frame)
        self.reloj.frame.pack(side=tk.RIGHT)

        # Tabla
        self.tabla_container = tk.Frame(self.main_frame)
        self.tabla_container.pack(fill=tk.BOTH, expand=True)

        self.tabla_citas = TablaCitas(self.tabla_container)

    def _ajustar_tabla(self, event=None):
        self.tabla_citas._ajustar_filas()

    def mostrar_datos(self, datos):
        self.tabla_citas.actualizar_datos(datos)