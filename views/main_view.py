import tkinter as tk
from views.components.reloj import Reloj
from views.components.tabla_citas import TablaCitas


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.fullscreen = False

        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        self.root.title("Citas para Área de Ventas")
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())

    def _crear_widgets(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        self.titulo = tk.Label(
            self.main_frame,
            text="Citas para Área de Ventas",
            font=('Helvetica', 16, 'bold')
        )
        self.titulo.pack(pady=(0, 10))

        # Reloj
        self.reloj = Reloj(self.main_frame)

        # Tabla de citas
        self.tabla_citas = TablaCitas(self.main_frame)

        # Botón de actualización
        self.actualizar_btn = tk.Button(
            self.main_frame,
            text="Actualizar",
            command=self.controller.actualizar_datos
        )
        self.actualizar_btn.pack(pady=10)

    def mostrar_datos(self, datos):
        self.tabla_citas.actualizar_datos(datos)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        if self.fullscreen:
            self.root.overrideredirect(True)
        else:
            self.root.overrideredirect(False)