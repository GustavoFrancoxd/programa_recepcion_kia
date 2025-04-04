class Cita:
    def __init__(self, cliente, fecha, hora, asesor):
        self.cliente = cliente
        self.fecha = fecha
        self.hora = hora
        self.asesor = asesor

    def to_dict(self):
        return {
            'cliente': self.cliente,
            'fecha': self.fecha,
            'hora': self.hora,
            'asesor': self.asesor
        }