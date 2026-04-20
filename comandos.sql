-- ==========================================
-- CREACIÓN DE TABLAS PRINCIPALES (Catálogos)
-- ==========================================

CREATE TABLE Instalaciones (
    id_instalacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200) NOT NULL,
    capacidad INT NOT NULL
);

CREATE TABLE Talleres (
    id_taller SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);

CREATE TABLE Concesionarias (
    id_concesionaria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200)
);

CREATE TABLE Clubes (
    id_club SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    representante VARCHAR(100)
);

CREATE TABLE Participantes (
    id_participante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    presupuesto DECIMAL(12, 2),
    correo VARCHAR(100) UNIQUE
);

-- ==========================================
-- CREACIÓN DE TABLAS CON LLAVES FORÁNEAS (FK)
-- ==========================================

CREATE TABLE Eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL, -- Crucial para filtrar los eventos de tipo "Tuning"
    id_instalacion INT REFERENCES Instalaciones(id_instalacion) ON DELETE SET NULL
);

CREATE TABLE Carros (
    id_carro SERIAL PRIMARY KEY,
    marca VARCHAR(50) NOT NULL, -- Necesario para "Catalogación de Carros"
    modelo VARCHAR(50) NOT NULL, -- Necesario para "Catalogación de Carros"
    anio INT NOT NULL,           -- Necesario para filtrar > 2022
    precio DECIMAL(12, 2) NOT NULL,
    estado VARCHAR(50) NOT NULL CHECK (estado IN ('Venta', 'Exposición', 'Compra')), -- Vital para filtrar
    id_dueno INT REFERENCES Participantes(id_participante) ON DELETE SET NULL
);

-- ==========================================
-- TABLAS INTERMEDIAS / TRANSACCIONALES
-- ==========================================

-- Tabla para resolver "Participación en Eventos" (Muchos a Muchos entre Clubes y Eventos)
CREATE TABLE Participaciones_Clubes (
    id_club INT REFERENCES Clubes(id_club) ON DELETE CASCADE,
    id_evento INT REFERENCES Eventos(id_evento) ON DELETE CASCADE,
    PRIMARY KEY (id_club, id_evento)
);

-- Tabla para resolver "Ventas por Concesionaria" y "Estatus de Participantes"
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_carro INT REFERENCES Carros(id_carro) ON DELETE RESTRICT,
    id_concesionaria INT REFERENCES Concesionarias(id_concesionaria) ON DELETE SET NULL,
    id_participante_comprador INT REFERENCES Participantes(id_participante) ON DELETE RESTRICT,
    monto DECIMAL(12, 2) NOT NULL, -- Registra cuánto gastó el participante / cuánto ingresó la concesionaria
    fecha_venta DATE DEFAULT CURRENT_DATE
);

-- Tabla para resolver "Carga de Trabajo en Talleres"
CREATE TABLE Reparaciones (
    id_reparacion SERIAL PRIMARY KEY,
    id_taller INT REFERENCES Talleres(id_taller) ON DELETE CASCADE,
    id_carro INT REFERENCES Carros(id_carro) ON DELETE CASCADE,
    id_evento INT REFERENCES Eventos(id_evento) ON DELETE CASCADE, -- Vincula la reparación con el evento específico
    descripcion TEXT,
    costo DECIMAL(10, 2),
    fecha_reparacion DATE DEFAULT CURRENT_DATE
);