from datetime import datetime

class ClaseGrupal:
    def __init__(self, id_clase, nombre_clase, instructor, horario, capacidad_maxima):
        self.id_clase = id_clase
        self.nombre_clase = nombre_clase
        self.instructor = instructor
        self.horario = horario
        self.capacidad_maxima = capacidad_maxima
        self.reservas = []  # lista de reservas asociadas a la clase

    def verificar_cupo_disponible(self):
        """Regla de negocio 4: Una clase no puede superar su capacidad maxima."""
        return len(self.reservas) < self.capacidad_maxima


class Reserva:
    def __init__(self, id_reserva, cliente, clase: ClaseGrupal):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.clase = clase
        self.fecha_reserva = datetime.now()
        self.estado = "Confirmada"

    def registrar_reserva(self):
        """valida las reglas de negocio antes de confirmar la reserva."""
        
        # regla de negocio 5: no permitir reserva duplicada del mismo cliente para la misma sesion
        for r in self.clase.reservas:
            if r.cliente.id_cliente == self.cliente.id_cliente:
                return False, "Error: el cliente ya tiene una reserva activa para esta clase."
        
        # regla de negocio 4: controlar capacidad maxima
        if not self.clase.verificar_cupo_disponible():
            return False, "Error: La clase ha alcanzado su capacidad maxima."
        
        # si pasa las validaciones, se añade la reserva
        self.clase.reservas.append(self)
        return True, "reserva registrada exitosamente."
    # Agregar al final de models/clase_reserva.py

class Asistencia:
    def __init__(self, id_asistencia, cliente, clase: ClaseGrupal):
        self.id_asistencia = id_asistencia
        self.cliente = cliente
        self.clase = clase
        self.fecha_registro = datetime.now()
        self.estado_asistencia = "Presente" # regla 6: asociada a sesión y cliente