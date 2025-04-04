from views.main_view import MainView
from models.google_sheets import GoogleSheetsManager


class CitasController:
    def __init__(self, root):
        self.root = root
        self.sheets_manager = GoogleSheetsManager()
        self.view = MainView(root, self)
        self.actualizar_datos()

    def actualizar_datos(self):
        """Obtiene citas del modelo y las envía a la vista"""
        datos = self.sheets_manager.obtener_citas_hoy()
        self.view.mostrar_datos(datos)
        # Reiniciar el ciclo de paginación con nuevos datos
        if hasattr(self.view.tabla_citas, 'detener_paginacion'):
            self.view.tabla_citas.detener_paginacion()
            self.view.tabla_citas.iniciar_paginacion()

    def toggle_fullscreen(self):
        """Alterna pantalla completa (se llama con la tecla ESC)"""
        self.view.toggle_fullscreen()