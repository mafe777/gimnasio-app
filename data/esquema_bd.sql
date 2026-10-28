-- ========================================================
-- CAPA DE BASE DE DATOS: Estructuras y Tablas Relacionales
-- ========================================================

CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE PlanesMembresia (
    id_plan INT PRIMARY KEY AUTO_INCREMENT,
    nombre_plan VARCHAR(50) NOT NULL,
    duracion_dias INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    beneficios TEXT
);

CREATE TABLE Membresias (
    id_membresia INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_plan INT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activa',
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_plan) REFERENCES PlanesMembresia(id_plan)
);

CREATE TABLE ClasesGrupales (
    id_clase INT PRIMARY KEY AUTO_INCREMENT,
    nombre_clase VARCHAR(50) NOT NULL,
    instructor VARCHAR(50) NOT NULL,
    horario VARCHAR(50) NOT NULL,
    capacidad_maxima INT NOT NULL
);

CREATE TABLE Reservas (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_clase INT,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Confirmada',
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_clase) REFERENCES ClasesGrupales(id_clase)
);