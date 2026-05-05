from errores import ReservaError
from logs import registrar_evento

class Reserva:
    def __init__(self, cliente, servicio):
        if not cliente:
            raise ReservaError("No se puede crear reserva sin un cliente activo")
        
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def costo(self):
        """Llama al método polimórfico del servicio"""
        return self.servicio.calcular_total()

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva cancelada")
        self.estado = "Confirmada"
        registrar_evento(f"Reserva confirmada para {self.cliente.cedula}")

    def cancelar(self):
        self.estado = "Cancelada"
        registrar_evento(f"Reserva cancelada para {self.cliente.cedula}")

    def __str__(self):
        return f"Reserva de {self.servicio.nombre}"