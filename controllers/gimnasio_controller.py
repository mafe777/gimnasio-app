# controllers/gimnasio_controller.py
from models.cliente import Cliente
from models.clase_reserva import Reserva
from data.repositorio import GimnasioRepositorio

class GimnasioController:
    def __init__(self, repositorio: GimnasioRepositorio):
        # inyección del repositorio 
        self.repositorio = repositorio

    def registrar_cliente_controller(self, id_cliente, nombre, apellido, correo, telefono):
        """Coordina el registro de un nuevo cliente."""
        nuevo_cliente = Cliente(id_cliente, nombre, apellido, correo, telefono)
        
        exito, mensaje_dal = self.repositorio.guardar_cliente(nuevo_cliente)
        
        if exito:
            return True, f"Controlador - Éxito: Cliente {nombre} registrado correctamente. [{mensaje_dal}]"
        else:
            return False, f"Controlador - Restricción de negocio: {mensaje_dal}"

    def reservar_clase_controller(self, id_reserva, id_cliente, clase_obj):
        """Coordina la regla de negocio para reservar una clase grupal."""
        cliente_encontrado = self.repositorio.buscar_cliente(id_cliente)
        
        if not cliente_encontrado:
            return "Error: El cliente no se encuentra registrado en el sistema."

        # crear la reserva y aplicar validaciones
        nueva_reserva = Reserva(id_reserva, cliente_encontrado, clase_obj)
        exito, mensaje = nueva_reserva.registrar_reserva()
        
        if exito:
            return f"Controlador - Éxito en la reserva: {mensaje}"
        else:
            return f"Controlador - Restricción de negocio: {mensaje}"