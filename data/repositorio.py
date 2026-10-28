# data/repositorio.py
# esta clase actua como nuestra Capa de acceso a Datos 
# simulando las operaciones de persistencia hacia una base de datos relacional

class GimnasioRepositorio:
    def __init__(self):
        # listas simuladas que actuan como tablas de la base de datos
        self.clientes = []
        self.membresias = []
        self.clases = []
        self.pagos = []
        self.asistencias = []

    # --- operaciones para clientes ---
    def guardar_cliente(self, cliente):
        # Validar si ya existe un cliente con el mismo correo
        for c in self.clientes:
            if c.correo == cliente.correo:
                return False, "Error: Ya existe un cliente registrado con este correo electrónico."
        
        self.clientes.append(cliente)
        return True, "Cliente guardado en la base de datos con éxito."

    def buscar_cliente(self, id_cliente):
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None

    # --- operaciones para Pagos ---
    def registrar_pago(self, pago):
        self.pagos.append(pago)
        return True, "Pago registrado en el historial de forma permanente."

    def obtener_historial_pagos(self, id_cliente):
        return [p for p in self.pagos if p.id_cliente == id_cliente]

    # --- operaciones para Clases y Asistencia ---
    def guardar_clase(self, clase):
        self.clases.append(clase)
        return "Clase grupal programada con éxito."
    
    def obtener_historial_pagos(self, id_cliente):
        return [p for p in self.pagos if p.id_cliente == id_cliente]
    # ---operaciones para membresias ---
    def guardar_membresia(self, membresia):
        self.membresias.append(membresia)
        return "membresia asignada y registrada con exito."

    def obtener_membresias_cliente(self, id_cliente):
        return [m for m in self.membresias if m.id_cliente == id_cliente]
    
    def actualizar_estado_cliente(self, id_cliente, nuevo_estado):
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            cliente.estado = nuevo_estado
            # Si el cliente pasa a inactivo, inactivamos sus membresías
            if nuevo_estado == "Inactivo":
                for m in self.membresias:
                    if m.id_cliente == id_cliente:
                        m.estado = "Suspendida / Inactiva"
            return True
        return False
    