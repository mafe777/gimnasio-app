# models/pago.py
from datetime import datetime

class Pago:
    def __init__(self, id_pago, id_cliente, monto, metodo_pago):
        self.id_pago = id_pago
        self.id_cliente = id_cliente
        self.monto = monto
        self.fecha_pago = datetime.now()
        self.metodo_pago = metodo_pago  # tarjeta, efectivo, transferencia
        self.estado = "Completado"  # regla 7: el estado no debe modificarse arbitrariamente una vez registrado

    def obtener_detalle(self):
        return {
            "id_pago": self.id_pago,
            "monto": self.monto,
            "fecha": self.fecha_pago.strftime("%Y-%m-%d %H:%M"),
            "estado": self.estado
        }