class Cliente:
    def __init__(self, id_cliente, nombre, apellido, correo, telefono, estado="Activo"):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.estado = estado  # activo o inactivo

    def registrar_cliente(self):
        # logica para registrar el cliente
        pass

    def actualizar_informacion(self, nuevo_correo, nuevo_telefono):
        self.correo = nuevo_correo
        self.telefono = nuevo_telefono

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado