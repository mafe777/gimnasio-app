from datetime import datetime, timedelta

class PlanMembresia:
    def __init__(self, id_plan, nombre_plan, duracion_dias, precio, beneficios):
        self.id_plan = id_plan
        self.nombre_plan = nombre_plan
        self.duracion_dias = duracion_dias
        self.precio = precio
        self.beneficios = beneficios


class Membresia:
    def __init__(self, id_membresia, id_cliente, plan: PlanMembresia, fecha_inicio=None):
        self.id_membresia = id_membresia
        self.id_cliente = id_cliente
        self.plan = plan
        self.fecha_inicio = fecha_inicio if fecha_inicio else datetime.now()
        #segun el plan y su duracion se calcula la finalizacion
        self.fecha_fin = self.fecha_inicio + timedelta(days=plan.duracion_dias)
        self.estado = "Activa"  # activa, vencida, cancelada

    def verificar_vencimiento(self):
        """Verifica si la membresía ha expirado según la fecha actual."""
        if datetime.now() > self.fecha_fin:
            self.estado = "Vencida"
        return self.estado