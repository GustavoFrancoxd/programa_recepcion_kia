from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheetsManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.KEY = 'key.json'
        self.SPREADSHEET_ID = '1Qd6jbfl2Zoi9dzYrt5Zn_h7t931ic4zjP3-bWI-roJ8'
        self.RANGO = "'CITAS 2025'!A2:P"  # Asegúrate que el nombre de la hoja es correcto
        self._service = None

    @property
    def service(self):
        if self._service is None:
            creds = service_account.Credentials.from_service_account_file(
                self.KEY, scopes=self.SCOPES)
            self._service = build('sheets', 'v4', credentials=creds)
        return self._service

    def obtener_citas_hoy(self):
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=self.RANGO
            ).execute()

            values = result.get('values', [])
            return self._filtrar_datos(values)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []

    def _filtrar_datos(self, values):
        """Filtra los datos según las columnas especificadas"""
        hoy = datetime.now().strftime('%d/%m/%Y')
        datos_filtrados = []

        for fila in values:
            try:
                # Verificar que la fila tenga suficientes columnas
                if len(fila) < 14:  # Necesitamos hasta la columna N (0-based index)
                    continue

                # Obtener valores de las columnas especificadas
                cliente = fila[2] if len(fila) > 2 else ''        # Columna C (índice 2)
                fecha_raw = fila[6] if len(fila) > 6 else ''      # Columna G (índice 6)
                hora = fila[7] if len(fila) > 7 else ''           # Columna H (índice 7)
                confirmada = fila[9].strip().upper() == 'TRUE' if len(fila) > 9 else False  # Columna J (índice 9)
                cancelada = fila[12].strip().upper() == 'TRUE' if len(fila) > 12 else False # Columna M (índice 12)
                asesor = fila[13] if len(fila) > 13 else ''       # Columna N (índice 13)

                # Procesar fecha
                try:
                    fecha_obj = datetime.strptime(fecha_raw, '%d/%m/%Y')
                    fecha = fecha_obj.strftime('%d/%m/%Y')
                except ValueError:
                    try:
                        fecha_obj = datetime.strptime(fecha_raw, '%m/%d/%Y')
                        fecha = fecha_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        fecha = ''

                # Filtrar citas de hoy confirmadas y no canceladas
                if fecha == hoy and confirmada and not cancelada:
                    datos_filtrados.append({
                        'cliente': cliente,
                        'fecha': fecha,
                        'hora': hora,
                        'asesor': asesor,
                        'confirmada': confirmada,
                        'cancelada': cancelada
                    })

            except Exception as e:
                print(f"Error procesando fila: {e}")
                continue

        return datos_filtrados