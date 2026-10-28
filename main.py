# main.py
from data.repositorio import GimnasioRepositorio
from controllers.gimnasio_controller import GimnasioController
from models.clase_reserva import ClaseGrupal

def ejecutar_simulacion():
    print("=== INICIANDO PLATAFORMA WEB DEL GIMNASIO ===")
    
    # 1. inicializar la capa de acceso a datos 
    repo = GimnasioRepositorio()
    
    # 2. inicializar el controlador 
    controller = GimnasioController(repo)
    
    # 3. registrar un cliente 
    print("\n--- PRUEBA 1: Registro de cliente ---")
    res_cliente = controller.registrar_cliente_controller(
        id_cliente=1, 
        nombre="Carlos", 
        apellido="Perez", 
        correo="carlos@mail.com", 
        telefono="3001234567"
    )
    print(res_cliente)
    
    # 4. programar una clase grupal con capacidad maxima de 1
    print("\n--- PRUEBA 2: programación de Clase y validación de reglas de negocio ---")
    clase_spinning = ClaseGrupal(
        id_clase=101, 
        nombre_clase="Spinning Avanzado", 
        instructor="Ana Gomez", 
        horario="Lunes 08:00 AM", 
        capacidad_maxima=1
    )
    repo.guardar_clase(clase_spinning)
    print(f"Clase creada: {clase_spinning.nombre_clase} (Capacidad maxima: {clase_spinning.capacidad_maxima})")
    
    # 5. primera reserva exitosa
    print("\n[Intento de reserva 1]:")
    resultado_reserva1 = controller.reservar_clase_controller(id_reserva=1, id_cliente=1, clase_obj=clase_spinning)
    print(resultado_reserva1)
    
    # 6. intentar reserva duplicada del mismo cliente 
    print("\n[Intento de reserva 2 - Mismo cliente duplicado]:")
    resultado_reserva2 = controller.reservar_clase_controller(id_reserva=2, id_cliente=1, clase_obj=clase_spinning)
    print(resultado_reserva2)

if __name__ == "__main__":
    ejecutar_simulacion()