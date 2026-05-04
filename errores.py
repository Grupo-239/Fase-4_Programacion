class ClienteError(Exception):
    pass

class ClienteExistenteError(ClienteError):
    pass

class ClienteNoEncontradoError(ClienteError):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


class SesionError(Exception):
    pass