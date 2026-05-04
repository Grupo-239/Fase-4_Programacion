from errores import ClienteError, ClienteExistenteError, ClienteNoEncontradoError

class Cliente:
    def __init__(self, nombre, cedula, correo):
        if not nombre:
            raise ClienteError("Nombre vacío")
        if not cedula.isdigit():
            raise ClienteError("Cédula inválida")
        if "@" not in correo:
            raise ClienteError("Correo inválido")

        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


class SistemaClientes:
    def __init__(self):
        self.clientes = []

    def registrar_cliente(self, nombre, cedula, correo):
        # Validar duplicado por cédula
        for c in self.clientes:
            if c.cedula == cedula:
                raise ClienteExistenteError("Cliente ya registrado")

        nuevo = Cliente(nombre, cedula, correo)
        self.clientes.append(nuevo)
        return nuevo

    def buscar_cliente(self, cedula):
        for c in self.clientes:
            if c.cedula == cedula:
                return c
        raise ClienteNoEncontradoError("Cliente no encontrado")