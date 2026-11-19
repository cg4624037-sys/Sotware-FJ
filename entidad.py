from abc import ABC, abstractmethod

# Clase abstracta general
class Entidad(ABC):

    def __init__(self, identificacion):
        if not identificacion:
            raise ValueError("La identificacion es obligatoria")

        self.__identificacion = identificacion

    # Propiedad para consultar identificacion
    @property
    def identificacion(self):
        return self.__identificacion

    # Metodo abstracto
    @abstractmethod
    def mostrar_informacion(self):
        pass