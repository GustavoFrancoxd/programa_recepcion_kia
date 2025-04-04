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
            return self._filtrar_datos(values)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []

    def _filtrar_datos(self, values):
        hoy = datetime.now().strftime('%d/%m/%Y')
        datos_filtrados = []

        for fila in values:
            if len(fila) >= 14:
                fecha = fila[5] if len(fila) > 5 else ''
                checkbox_i = fila[8].lower() == 'true' if len(fila) > 8 else False
                checkbox_m = fila[12].lower() == 'true' if len(fila) > 12 else False

                if fecha == hoy and checkbox_i and not checkbox_m:
                    cliente = fila[1] if len(fila) > 1 else ''
                    hora = fila[6] if len(fila) > 6 else ''
                    asesor = fila[13] if len(fila) > 13 else ''
                    datos_filtrados.append({
                        'cliente': cliente,
                        'fecha': fecha,
                        'hora': hora,
                        'asesor': asesor
                    })
        return datos_filtrados