from entidad import Entidad
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError
)
from logs import registrar_evento, registrar_error


class Reserva(Entidad):

    def __init__(self, identificacion, cliente, servicio, duracion, **parametros):

        super().__init__(identificacion)

        if cliente is None:
            raise ReservaInvalidaError("Debe seleccionar un cliente")

        if servicio is None:
            raise ReservaInvalidaError("Debe seleccionar un servicio")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__parametros = parametros
        self.__estado = "Pendiente"
        self.__costo = 0

        servicio.validar_parametros(duracion, **parametros)

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self):

        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solamente se pueden confirmar reservas pendientes"
            )

        self.__servicio.verificar_disponibilidad()

        self.__estado = "Confirmada"
        registrar_evento(f"Reserva {self.identificacion} confirmada")

    def cancelar(self):

        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva que no esta pendiente"
            )

        self.__estado = "Cancelada"
        registrar_evento(f"Reserva {self.identificacion} cancelada")

    def procesar(self, impuesto=0, descuento=0):

        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada para procesarse"
            )

        try:
            self.__costo = self.__servicio.calcular_costo(
                self.__duracion,
                impuesto,
                descuento,
                **self.__parametros
            )

            if self.__costo < 0:
                raise ReservaInvalidaError("El costo calculado no puede ser negativo")

            registrar_evento(
                f"Reserva {self.identificacion} procesada. "
                f"Costo: ${self.__costo:,.2f}"
            )

            return self.__costo

        except Exception as error:
            registrar_error(
                f"Error procesando reserva {self.identificacion}: {error}"
            )

            # Encadenamiento de excepciones
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error

    def mostrar_informacion(self):

        return (
            f"Reserva: {self.identificacion}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion}\n"
            f"Estado: {self.__estado}\n"
            f"Costo: ${self.__costo:,.2f}"
        )