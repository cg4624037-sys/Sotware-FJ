# Excepcion base del sistema
class ErrorSistema(Exception):
    pass


# Error cuando los datos ingresados no son validos
class DatosInvalidosError(ErrorSistema):
    pass


# Error cuando un servicio no esta disponible
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Error cuando una reserva no puede realizarse
class ReservaInvalidaError(ErrorSistema):
    pass


# Error cuando se intenta realizar una operacion no permitida
class OperacionNoPermitidaError(ErrorSistema):
    pass