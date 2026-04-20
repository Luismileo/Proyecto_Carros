-- 1. INSTALACIONES
INSERT INTO Instalaciones (nombre, ubicacion, capacidad) VALUES 
('Autódromo Los Próceres', 'Caracas', 5000),
('Circuito Turagua', 'Aragua', 8000),
('Pista La Chinita', 'Maracaibo', 3500);

-- 2. TALLERES
INSERT INTO Talleres (nombre, especialidad) VALUES 
('Tuning Master', 'Modificaciones'),
('Reparaciones Express', 'Mecánica General'),
('Pintura y Estilo', 'Estética');

-- 3. CONCESIONARIAS
INSERT INTO Concesionarias (nombre, ubicacion) VALUES 
('Luxury Cars', 'Las Mercedes'),
('AutoVentas Oriente', 'Puerto La Cruz'),
('Multimarca Center', 'Valencia');

-- 4. CLUBES
INSERT INTO Clubes (nombre, representante) VALUES 
('Team JDM Venezuela', 'Carlos Ruiz'),
('Classic Racing Club', 'Elena Mendez'),
('Tuning Caracas 212', 'Ricardo Sanz');

-- 5. PARTICIPANTES
INSERT INTO Participantes (nombre, presupuesto, correo) VALUES 
('Andrés Bello', 45000, 'andres@email.com'),
('Simón Bolívar', 15000, 'simon@email.com'),
('Luisa Cáceres', 60000, 'luisa@email.com'),
('Francisco Miranda', 25000, 'fran@email.com');

-- 6. EVENTOS (Importante: Mezcla de Tipos)
INSERT INTO Eventos (nombre, fecha, tipo, id_instalacion) VALUES 
('Expo Tuning 2026', '2026-05-15', 'Tuning', 1),
('Gran Carrera de Mayo', '2026-05-20', 'Carrera', 2),
('Tuning Show Nocturno', '2026-06-10', 'Tuning', 1),
('Festival de Sonido (Tuning)', '2026-07-05', 'Tuning', 3);

-- 7. CARROS (Catalogación > 2022 y Estados)
INSERT INTO Carros (marca, modelo, anio, precio, estado, id_dueno) VALUES 
('Toyota', 'Supra', 2024, 55000, 'Exposición', 3),
('Honda', 'Civic Type R', 2023, 42000, 'Exposición', 1),
('Mazda', 'RX-7', 1998, 30000, 'Venta', NULL),
('Porsche', '911 GT3', 2025, 120000, 'Compra', 3),
('Nissan', 'GTR', 2022, 95000, 'Exposición', 4);

-- 8. PARTICIPACIONES EN EVENTOS (Para que algunos clubes tengan > 2)
-- El club 'Team JDM Venezuela' participará en 3 eventos de Tuning
INSERT INTO Participaciones_Clubes (id_club, id_evento) VALUES (1, 1), (1, 3), (1, 4);
-- Otros clubes con menos participaciones
INSERT INTO Participaciones_Clubes (id_club, id_evento) VALUES (2, 1), (3, 4);

-- 9. VENTAS (Para validar ingresos y gastos > $30,000)
INSERT INTO Ventas (id_carro, id_concesionaria, id_participante_comprador, monto) VALUES 
(4, 1, 3, 120000), -- Venta de Porsche a Luisa (Gasto > 30k)
(2, 1, 1, 42000);   -- Venta de Honda a Andrés (Gasto > 30k)

-- 10. REPARACIONES (Carga de trabajo en talleres para un evento específico)
-- Reparaciones vinculadas al evento ID 1 (Expo Tuning 2026)
INSERT INTO Reparaciones (id_taller, id_carro, id_evento, descripcion, costo) VALUES 
(1, 1, 1, 'Ajuste de turbo', 1500),
(1, 2, 1, 'Cambio de suspensión', 2000),
(2, 3, 1, 'Revisión de motor', 500);