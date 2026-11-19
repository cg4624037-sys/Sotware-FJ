from abc import abstractmethod
from entidad import Entidad
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError
)


# Clase abstracta Servicio
class Servicio(Entidad):

    def __init__(self, identificacion, nombre, precio, disponible=True):

        super().__init__(identificacion)

        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio")

        if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero")

        self.__nombre = nombre
        self.__precio = precio
        self.__disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    @property
    def disponible(self):
        return self.__disponible

    def verificar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.__nombre} no esta disponible"
            )

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("La disponibilidad debe ser True o False")
        self.__disponible = estado

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):
        pass

    @abstractmethod
    def validar_parametros(self, duracion, **parametros):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def mostrar_informacion(self):
        return self.describir_servicio()


# Servicio especializado: reserva de salas
class ReservaSala(Servicio):

    def validar_parametros(self, duracion, **parametros):

        self.verificar_disponibilidad()

        capacidad = parametros.get("capacidad", 1)

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo")

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):

        self.validar_parametros(duracion, **parametros)
        subtotal = self.precio * duracion

        return subtotal + (subtotal * impuesto / 100) - (subtotal * descuento / 100)

    def describir_servicio(self):
        return f"Sala: {self.nombre} | Tarifa por hora: ${self.precio:,.2f}"


# Servicio especializado: alquiler de equipos
class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion, **parametros):

        self.verificar_disponibilidad()

        cantidad = parametros.get("cantidad", 1)

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser un entero positivo")

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):

        self.validar_parametros(duracion, **parametros)
        cantidad = parametros.get("cantidad", 1)

        subtotal = self.precio * duracion * cantidad

        return subtotal + (subtotal * impuesto / 100) - (subtotal * descuento / 100)

    def describir_servicio(self):
        return f"Equipo: {self.nombre} | Tarifa por dia: ${self.precio:,.2f}"


# Servicio especializado: asesoria especializada
class Asesoria(Servicio):

    def validar_parametros(self, duracion, **parametros):

        self.verificar_disponibilidad()

        modalidad = parametros.get("modalidad", "virtual")

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas de asesoria deben ser positivas")

        if modalidad not in ("virtual", "presencial"):
            raise DatosInvalidosError("La modalidad debe ser virtual o presencial")

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **parametros):

        self.validar_parametros(duracion, **parametros)
        modalidad = parametros.get("modalidad", "virtual")

        subtotal = self.precio * duracion

        # La asesoria presencial tiene un recargo del 10 %
        if modalidad == "presencial":
            subtotal *= 1.10

        return subtotal + (subtotal * impuesto / 100) - (subtotal * descuento / 100)

    def describir_servicio(self):
        return f"Asesoria: {self.nombre} | Tarifa por hora: ${self.precio:,.2f}"