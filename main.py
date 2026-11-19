from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import ErrorSistema
from logs import registrar_evento, registrar_error


# Listas internas del sistema
clientes = []
servicios = []
reservas = []


# Funcion para registrar clientes
def registrar_cliente(cliente):

    if any(c.identificacion == cliente.identificacion for c in clientes):
        raise ValueError("El cliente ya se encuentra registrado")

    clientes.append(cliente)
    registrar_evento(f"Cliente registrado: {cliente.nombre}")


# Funcion para registrar servicios
def registrar_servicio(servicio):

    if any(s.identificacion == servicio.identificacion for s in servicios):
        raise ValueError("El servicio ya se encuentra registrado")

    servicios.append(servicio)
    registrar_evento(f"Servicio registrado: {servicio.nombre}")


# Funcion para registrar reservas
def registrar_reserva(reserva):

    if any(r.identificacion == reserva.identificacion for r in reservas):
        raise ValueError("La reserva ya existe")

    reservas.append(reserva)
    registrar_evento(f"Reserva creada: {reserva.identificacion}")


# Funcion para ejecutar operaciones sin detener el programa
def ejecutar_operacion(descripcion, funcion):

    print(f"\n--- {descripcion} ---")

    try:
        funcion()

    except (ErrorSistema, ValueError, TypeError) as error:
        print(f"Error controlado: {error}")
        registrar_error(f"{descripcion}: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")
        registrar_error(f"Error inesperado en {descripcion}: {error}")

    else:
        print("Operacion realizada correctamente")

    finally:
        print("Operacion finalizada. El sistema continua activo.")


# Operacion 1: registrar cliente correctamente
def operacion_1():

    cliente = Cliente(
        "101",
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3001234567"
    )

    registrar_cliente(cliente)
    print(cliente.mostrar_informacion())


# Operacion 2: registrar otro cliente
def operacion_2():

    cliente = Cliente(
        "102",
        "Maria Lopez",
        "maria@gmail.com",
        "3101234567"
    )

    registrar_cliente(cliente)
    print(cliente.mostrar_informacion())


# Operacion 3: registrar cliente con correo invalido
def operacion_3():

    cliente = Cliente(
        "103",
        "Pedro Gomez",
        "correo_incorrecto",
        "3201234567"
    )

    registrar_cliente(cliente)


# Operacion 4: crear servicio de sala
def operacion_4():

    sala = ReservaSala(
        "S01",
        "Sala de conferencias",
        50000
    )

    registrar_servicio(sala)
    print(sala.describir_servicio())


# Operacion 5: crear servicio de alquiler de equipos
def operacion_5():

    equipo = AlquilerEquipo(
        "E01",
        "Proyector multimedia",
        80000
    )

    registrar_servicio(equipo)
    print(equipo.describir_servicio())


# Operacion 6: crear servicio de asesoria
def operacion_6():

    asesoria = Asesoria(
        "A01",
        "Asesoria en desarrollo de software",
        100000
    )

    registrar_servicio(asesoria)
    print(asesoria.describir_servicio())


# Operacion 7: intentar crear un servicio con precio invalido
def operacion_7():

    sala = ReservaSala(
        "S02",
        "Sala secundaria",
        -20000
    )

    registrar_servicio(sala)


# Operacion 8: crear y procesar una reserva correctamente
def operacion_8():

    cliente = clientes[0]
    servicio = servicios[0]

    reserva = Reserva(
        "R01",
        cliente,
        servicio,
        3,
        capacidad=20
    )

    registrar_reserva(reserva)
    reserva.confirmar()

    costo = reserva.procesar(impuesto=19, descuento=5)

    print(reserva.mostrar_informacion())
    print(f"Costo final: ${costo:,.2f}")


# Operacion 9: intentar realizar una reserva con duracion invalida
def operacion_9():

    reserva = Reserva(
        "R02",
        clientes[1],
        servicios[1],
        -2,
        cantidad=1
    )

    registrar_reserva(reserva)


# Operacion 10: intentar utilizar un servicio no disponible
def operacion_10():

    servicio = servicios[1]
    servicio.cambiar_disponibilidad(False)

    reserva = Reserva(
        "R03",
        clientes[1],
        servicio,
        2,
        cantidad=1
    )

    registrar_reserva(reserva)


# Operacion 11: cancelar una reserva
def operacion_11():

    reserva = Reserva(
        "R04",
        clientes[1],
        servicios[2],
        2,
        modalidad="virtual"
    )

    registrar_reserva(reserva)
    reserva.cancelar()

    print(reserva.mostrar_informacion())


# Operacion 12: intentar procesar una reserva sin confirmar
def operacion_12():

    reserva = Reserva(
        "R05",
        clientes[0],
        servicios[2],
        2,
        modalidad="presencial"
    )

    registrar_reserva(reserva)
    reserva.procesar()


# Ejecucion del sistema
if __name__ == "__main__":

    print("==========================================")
    print(" SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("==========================================")

    registrar_evento("Inicio del sistema Software FJ")

    operaciones = [
        ("Registro de cliente 1", operacion_1),
        ("Registro de cliente 2", operacion_2),
        ("Registro de cliente invalido", operacion_3),
        ("Creacion de sala", operacion_4),
        ("Creacion de equipo", operacion_5),
        ("Creacion de asesoria", operacion_6),
        ("Creacion de servicio invalido", operacion_7),
        ("Reserva exitosa", operacion_8),
        ("Reserva con duracion invalida", operacion_9),
        ("Servicio no disponible", operacion_10),
        ("Cancelacion de reserva", operacion_11),
        ("Procesamiento sin confirmar", operacion_12)
    ]

    for descripcion, funcion in operaciones:
        ejecutar_operacion(descripcion, funcion)

    print("\n==========================================")
    print(" RESUMEN GENERAL DEL SISTEMA")
    print("==========================================")

    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios registrados: {len(servicios)}")
    print(f"Reservas registradas: {len(reservas)}")

    print("\nReservas realizadas:")

    for reserva in reservas:
        print(
            f"{reserva.identificacion} - "
            f"Estado: {reserva.estado}"
        )

    registrar_evento("Finalizacion de las operaciones del sistema")

    print("\nEl sistema finalizo correctamente.")
    print("Los eventos y errores se encuentran en logs_sistema.txt")