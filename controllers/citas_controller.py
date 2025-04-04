from views.main_view import MainView
from models.google_sheets import GoogleSheetsManager
from models.cache_manager import CacheManager
from datetime import datetime



class CitasController:
    def __init__(self, root):
        self.root = root
        self.sheets_manager = GoogleSheetsManager()
        self.cache = CacheManager()
        self.ultima_peticion = None
        self.contador_peticiones = 0

        # Inicializar vista
        self.view = MainView(root, self)

        # Cargar datos iniciales
        self._safe_actualizar_datos()

        # Programar actualizaciones periódicas
        self._programar_actualizaciones()

    def _safe_actualizar_datos(self):
        try:
            self.actualizar_datos()
        except Exception as e:
            print(f"Error al actualizar datos: {e}")

    def actualizar_datos(self):
        """Muestra información de la petición en terminal antes de realizarla"""
        print("\n" + "=" * 50)
        print(f"Iniciando petición a Google Sheets...")
        print(f"Hora actual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        try:
            datos = self.sheets_manager.obtener_citas_hoy()
            self.contador_peticiones += 1
            self.ultima_peticion = datetime.now()

            print(f"\n✅ Petición exitosa")
            print(f"Total citas obtenidas: {len(datos)}")
            print(f"Última petición: {self.ultima_peticion.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Total peticiones en esta sesión: {self.contador_peticiones}")

            self.view.mostrar_datos(datos)
            return datos

        except Exception as e:
            print(f"\n❌ Error en la petición: {str(e)}")
            return []

    def _actualizar_en_segundo_plano(self):
        """Actualiza los datos en segundo plano"""
        try:
            datos = self.sheets_manager.obtener_citas_hoy()
            self.cache.update_cache(datos)
            # Actualizar vista en el hilo principal
            self.root.after(0, lambda: self.view.mostrar_datos(datos))
        except Exception as e:
            print(f"Error en actualización en segundo plano: {e}")

    def _programar_actualizaciones(self):
        """Programa actualizaciones periódicas cada 15 minutos"""
        self.actualizar_datos()
        self.root.after(900000, self._programar_actualizaciones)  # 15 minutos = 900,000 ms

    def toggle_fullscreen(self):
        self.view.toggle_fullscreen()