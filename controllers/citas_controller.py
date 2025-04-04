from views.main_view import MainView
from models.google_sheets import GoogleSheetsManager


class CitasController:
    def __init__(self, root):
        self.root = root
        self.sheets_manager = GoogleSheetsManager()

        # Inicializar vista
        self.view = MainView(root, self)

        # Cargar datos iniciales
        self.actualizar_datos()

    def actualizar_datos(self):
        datos = self.sheets_manager.obtener_citas_hoy()
        self.view.mostrar_datos(datos)

    def toggle_fullscreen(self):
        self.view.toggle_fullscreen()