from flask import Flask, render_template, request, redirect, url_for
from data.repositorio import GimnasioRepositorio
from controllers.gimnasio_controller import GimnasioController
from models.cliente import Cliente
from models.membresia import PlanMembresia, Membresia
from models.clase_reserva import ClaseGrupal, Reserva, Asistencia
from models.pago import Pago

app = Flask(__name__, template_folder='views/templates')

repo = GimnasioRepositorio()
controller = GimnasioController(repo)

# Planes de membresía oficiales
planes_disponibles = [
    PlanMembresia(id_plan=1, nombre_plan="Plan Básico Mensual", duracion_dias=30, precio=80000, beneficios="Acceso libre a pesas"),
    PlanMembresia(id_plan=2, nombre_plan="Plan Trimestral Pro", duracion_dias=90, precio=210000, beneficios="Pesas + Clases Grupales"),
    PlanMembresia(id_plan=3, nombre_plan="Plan Anual VIP", duracion_dias=365, precio=750000, beneficios="Acceso total + Invitados")
]

# Clase inicial de prueba
clase_inicial = ClaseGrupal(id_clase=101, nombre_clase="Spinning Avanzado", instructor="Carlos M.", horario="Lunes, Miércoles - 08:00 AM", capacidad_maxima=2)
repo.guardar_clase(clase_inicial)

@app.route('/')
def home():
    return render_template('index.html', 
                           clientes=repo.clientes, 
                           clases=repo.clases, 
                           pagos=repo.pagos, 
                           membresias=repo.membresias,
                           reservas=repo.reservas if hasattr(repo, 'reservas') else [],
                           asistencias=repo.asistencias,
                           planes=planes_disponibles)

# Gestión de Clientes (Registro)
@app.route('/registrar-cliente', methods=['POST'])
def registrar_cliente_web():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    telefono = request.form['telefono']
    id_asignado = len(repo.clientes) + 1
    
    controller.registrar_cliente_controller(
        id_cliente=id_asignado, nombre=nombre, apellido=apellido, correo=correo, telefono=telefono
    )
    # Redirigimos a la misma pestaña pasando el ID asignado por parámetro URL
    return redirect(url_for('home', id_creado=id_asignado, nombre_creado=nombre))

# Actualizar información o estado del cliente
@app.route('/actualizar-cliente/<int:id_cliente>', methods=['POST'])
def actualizar_cliente(id_cliente):
    cliente = repo.buscar_cliente(id_cliente)
    if cliente:
        cliente.nombre = request.form['nombre']
        cliente.apellido = request.form['apellido']
        cliente.correo = request.form['correo']
        cliente.telefono = request.form['telefono']
        nuevo_estado = request.form['estado']
        
        # Sincronizamos usando el repositorio
        repo.actualizar_estado_cliente(id_cliente, nuevo_estado)
        
    return redirect(url_for('home'))

# Gestión de Membresías
@app.route('/asignar-membresia', methods=['POST'])
def asignar_membresia_web():
    id_cliente = int(request.form['id_cliente'])
    id_plan = int(request.form['id_plan'])
    
    cliente = repo.buscar_cliente(id_cliente)
    plan_seleccionado = next((p for p in planes_disponibles if p.id_plan == id_plan), None)
    
    if cliente and plan_seleccionado:
        nueva_membresia = Membresia(id_membresia=len(repo.membresias)+1, id_cliente=id_cliente, plan=plan_seleccionado)
        repo.membresias.append(nueva_membresia)
        
    # Redirige de vuelta a la pestaña de membresías sin cuadros molestos
    return redirect(url_for('home'))

# Gestión de Pagos con cálculo de saldo pendiente
@app.route('/registrar-pago', methods=['POST'])
def registrar_pago_web():
    id_cliente = int(request.form['id_cliente'])
    monto = float(request.form['monto'])
    metodo = request.form['metodo']
    
    membresia_cliente = next((m for m in repo.membresias if m.id_cliente == id_cliente and m.estado == "Activa"), None)
    costo_plan = membresia_cliente.plan.precio if membresia_cliente else 80000
    
    pagos_previos = sum(p.monto for p in repo.pagos if p.id_cliente == id_cliente)
    total_abonado = pagos_previos + monto
    saldo_pendiente = max(0, costo_plan - total_abonado)
    
    estado_pago = "Completado" if saldo_pendiente == 0 else f"Pendiente (Resta: ${saldo_pendiente:,.0f})"
    
    nuevo_pago = Pago(id_pago=len(repo.pagos)+1, id_cliente=id_cliente, monto=monto, metodo_pago=metodo)
    nuevo_pago.estado = estado_pago
    repo.pagos.append(nuevo_pago)
    
    # Redirige directo a la pestaña de pagos sin pantallas intermedias
    return redirect(url_for('home'))

# Programación de Clases con selección de múltiples días (Checkboxes)
@app.route('/programar-clase', methods=['POST'])
def programar_clase_web():
    nombre = request.form['nombre_clase']
    instructor = request.form['instructor']
    dias = request.form.getlist('dias')  # Recibe múltiples días seleccionados
    hora = request.form['hora']
    capacidad = int(request.form['capacidad'])
    
    dias_str = ", ".join(dias) if dias else "Sin días"
    horario_formateado = f"{dias_str} - {hora}"
    
    nueva_clase = ClaseGrupal(id_clase=len(repo.clases)+101, nombre_clase=nombre, instructor=instructor, horario=horario_formateado, capacidad_maxima=capacidad)
    repo.guardar_clase(nueva_clase)
    return retornar_respuesta(True, f"Clase '{nombre}' programada correctamente.", f"Días: {dias_str} | Hora: {hora} | Cupos: {capacidad}")

# Reservas de Cupos
@app.route('/reservar-clase', methods=['POST'])
def reservar_clase_web():
    id_cliente = int(request.form['id_cliente'])
    id_clase = int(request.form['id_clase'])
    
    cliente = repo.buscar_cliente(id_cliente)
    clase_obj = next((c for c in repo.clases if c.id_clase == id_clase), None)
    
    if cliente and clase_obj:
        if not hasattr(repo, 'reservas'):
            repo.reservas = []
        reserva = Reserva(id_reserva=len(repo.reservas)+1, cliente=cliente, clase=clase_obj)
        exito, mensaje = reserva.registrar_reserva()
        if exito:
            repo.reservas.append(reserva)
            
    return redirect(url_for('home'))

# Cancelar Reserva
@app.route('/cancelar-reserva/<int:id_reserva>', methods=['POST'])
def cancelar_reserva(id_reserva):
    if hasattr(repo, 'reservas'):
        repo.reservas = [r for r in repo.reservas if r.id_reserva != id_reserva]
    return redirect(url_for('home'))

# Registrar Asistencia
@app.route('/registrar-asistencia', methods=['POST'])
def registrar_asistencia_web():
    id_cliente = int(request.form['id_cliente'])
    id_clase = int(request.form['id_clase'])
    
    cliente = repo.buscar_cliente(id_cliente)
    clase_obj = next((c for c in repo.clases if c.id_clase == id_clase), None)
    
    if cliente and clase_obj:
        asistencia = Asistencia(id_asistencia=len(repo.asistencias)+1, cliente=cliente, clase=clase_obj)
        repo.asistencias.append(asistencia)
        
    return redirect(url_for('home'))
def retornar_respuesta(exito, mensaje, extra):
    color = "#28a745" if exito else "#dc3545"
    return f"""
    <div style="font-family: Arial; margin: 40px; padding: 25px; border: 1px solid #ccc; border-radius: 8px; max-width: 500px; background: white;">
        <h2 style="color: {color};">{"¡Operación Exitosa!" if exito else "¡Restricción de Negocio!"}</h2>
        <p><b>Mensaje:</b> {mensaje}</p>
        <p style="font-size: 16px; color: #007bff;">{extra}</p>
        <br>
        <a href="/" style="background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block;">Volver al Sistema</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)