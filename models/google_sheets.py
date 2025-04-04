from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleSheetsManager:
    def __init__(self):
        # Configuración de Google Sheets
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.KEY = 'key.json'
        self.SPREADSHEET_ID = '1IJ5zeZMb5R5t8ftEIvP1V74gcckQkQkZi_JjSCOw4ss'

    def obtener_citas_hoy(self):
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.KEY, scopes=self.SCOPES)
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()

            result = sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range='Hoja 1!A2:O'
            ).execute()

            values = result.get('values', [])
            #print(values)
            print(self._filtrar_datos(values))
            return self._filtrar_datos(values)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []



    def _filtrar_datos(self, values):
        # Obtén la fecha actual en formato DD/MM/YYYY
        hoy = datetime.now().strftime('%d/%m/%Y')
        datos_filtrados = []

        for fila in values:
            if len(fila) >= 14:
                # Extrae la fecha cruda (ej: '3/8/2024')
                fecha_raw = fila[5] if len(fila) > 5 else ''

                # Intenta parsear la fecha en DOS formatos posibles
                try:
                    # Intenta como DD/MM/YYYY (ej: '8/3/2024' → 8 de marzo)
                    fecha_obj = datetime.strptime(fecha_raw, '%d/%m/%Y')
                    fecha = fecha_obj.strftime('%d/%m/%Y')  # Formatea a DD/MM/YYYY
                except ValueError:
                    try:
                        # Si falla, intenta como MM/DD/YYYY (ej: '3/8/2024' → 3 de agosto)
                        fecha_obj = datetime.strptime(fecha_raw, '%m/%d/%Y')
                        fecha = fecha_obj.strftime('%d/%m/%Y')  # Convierte a DD/MM/YYYY
                    except ValueError:
                        fecha = ''  # Si no es ninguna, descarta la fila

                checkbox_i = str(fila[8]).strip().upper() == 'TRUE' if len(fila) > 8 else False
                checkbox_m = str(fila[12]).strip().upper() == 'TRUE' if len(fila) > 12 else False

                if fecha == hoy and checkbox_i and not checkbox_m:
                    datos_filtrados.append({
                        'cliente': fila[1] if len(fila) > 1 else '',
                        'fecha': fecha,
                        'hora': fila[6] if len(fila) > 6 else '',
                        'asesor': fila[13] if len(fila) > 13 else ''
                    })

        return datos_filtrados