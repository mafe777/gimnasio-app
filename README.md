#  Sistema Centralizado de Gestión del Gimnasio

Plataforma web para la administración centralizada de clientes, membresías, pagos, clases grupales, reservas y asistencia.

---

##  Requisitos e Instrucciones de Ejecución

Para ejecutar la aplicación localmente, sigue estos pasos:

### 1. Requisitos Previos
* Tener instalado Python 3.8+
* Tener instalada la librería Flask

### 2. Instalación de Dependencias
Abre una terminal en la carpeta principal del proyecto y ejecuta:
pip install flask

### 3. Ejecución del Servidor
Inicia la aplicación ejecutando el comando principal:
python app.py

copia y pega la direccion que sale en la terminal en el navegador web

---

##  CUESTIONARIO DEL TALLER

### 1. ¿Cómo se distribuyen las responsabilidades en cada diseño?
* **Arquitectura en Capas:** Las responsabilidades se distribuyen de manera vertical de acuerdo con el tipo de acceso y procesamiento. La capa de presentación se ocupa de la interfaz web y de los formularios, la capa de negocio se encarga de gestionar las reglas del sistema y de validaciones, y la capa de acceso a datos tiene la responsabilidad de mantener la información y comunicarse con la base de datos.
* **Patrón MVC:** Las tareas se separan según los elementos visuales e interactivos. La vista presenta la información al usuario, el controlador recibe las solicitudes del usuario y organiza lo que se debe hacer, y el modelo alberga los datos y las normas del negocio, como los clientes, clases y pagos.

---

### 2. ¿Dónde ubicaría la regla que impide reservar una clase sin cupos?
Esta norma empresarial debe estar posicionada de manera precisa en la **capa de negocio / controlador**. No debe validarse solo en la interfaz gráfica, ya que un usuario podría evadir la vista. El backend tiene la responsabilidad de confirmar el límite máximo antes de aceptar o denegar la reserva en el repositorio.

---

### 3. ¿Qué componente deberá consultar los pagos registrados?
El componente responsable de verificar los pagos es la **capa de acceso a datos (el repositorio)** mediante el modelo, que es llamado por el controlador al recibir la solicitud de la vista para mostrar el historial. El repositorio localiza los datos almacenados y se los envía al controlador para que los muestre en la tabla de la interfaz.

---

### 4. ¿Qué cambios podrían realizarse en la interfaz sin modificar las reglas del negocio? (Dé 3 ejemplos)
Dado que la arquitectura distingue entre lo visual y lo lógico, es posible modificar por completo la apariencia de la pantalla sin impactar en el sistema. Tres ejemplos claros son:
1. Alterar los colores de los botones o de la barra lateral de morado a azul o verde.
2. Reorganizar la ubicación de los campos en un formulario, por ejemplo, colocar el apellido antes del nombre.
3. Sustituir las tablas HTML convencionales por tarjetas emergentes o gráficos estadísticos modernos sin modificar en absoluto los cálculos de saldos ni las reglas de las clases.

---

### 5. ¿Es posible utilizar MVC dentro de una arquitectura en capas? Justifique su respuesta.
**Sí es posible.** De hecho, es una práctica excelente y ampliamente empleada. La arquitectura por capas distribuye todo el software de manera general (presentación, negocio y datos), mientras que el patrón MVC se utiliza en particular en la capa de presentación y negocio para organizar la interacción entre las pantallas, las solicitudes web y los datos. En este proyecto se usó Flask exactamente según este modelo: las vistas HTML, los controladores de rutas y los modelos de datos coexisten de manera armoniosa dentro de una estructura por capas.


