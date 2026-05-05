from abc import ABC, abstractmethod
from errores import ServicioError

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_total(self):
        pass

class ReservaSala(Servicio):
    def __init__(self, horas, precio_base):
        super().__init__("Sala", precio_base)
        if horas <= 0: raise ServicioError("Las horas deben ser mayores a 0")
        self.horas = horas

    def calcular_total(self):
        # Polimorfismo: Pago por horas
        return self.precio_base * self.horas

class AlquilerEquipo(Servicio):
    def __init__(self, dias, precio_base):
        super().__init__("Equipo", precio_base)
        if dias <= 0: raise ServicioError("Los días deben ser mayores a 0")
        self.dias = dias

    def calcular_total(self):
        # Polimorfismo: Pago por días
        return self.precio_base * self.dias

class Asesoria(Servicio):
    def __init__(self, horas, precio_base):
        super().__init__("Asesoria", precio_base)
        if horas <= 0: raise ServicioError("Las horas de asesoría deben ser mayores a 0")
        self.horas = horas

    def calcular_total(self):
        # Polimorfismo: Pago por sesión/horas
        return self.precio_base * self.horas