-- 1. Ventas por Concesionaria
SELECT c.nombre, SUM(v.monto) as ingreso_total
FROM Concesionarias c
JOIN Ventas v ON c.id_concesionaria = v.id_concesionaria
GROUP BY c.nombre
ORDER BY ingreso_total DESC;

-- 2. Participación en Eventos (Clubes con > 2 eventos Tuning)
SELECT cl.nombre, COUNT(pc.id_evento) as cantidad_tuning
FROM Clubes cl
JOIN Participaciones_Clubes pc ON cl.id_club = pc.id_club
JOIN Eventos e ON pc.id_evento = e.id_evento
WHERE e.tipo = 'Tuning'
GROUP BY cl.nombre
HAVING COUNT(pc.id_evento) > 2;

-- 3. Catalogación de Carros (Exposición, Año > 2022)
SELECT marca, modelo, anio
FROM Carros
WHERE estado = 'Exposición' AND anio > 2022
ORDER BY marca ASC;

-- 4. Carga de Trabajo en Talleres (Para un evento específico, ej: ID 1)
SELECT t.nombre, COUNT(r.id_reparacion) as total_reparaciones
FROM Talleres t
JOIN Reparaciones r ON t.id_taller = r.id_taller
WHERE r.id_evento = 1 -- Aquí puedes cambiar el ID según el evento
GROUP BY t.nombre
ORDER BY total_reparaciones DESC;

-- 5. Estatus de Participantes (Gasto > $30,000)
SELECT p.nombre, SUM(v.monto) as total_gastado
FROM Participantes p
JOIN Ventas v ON p.id_participante = v.id_participante_comprador
GROUP BY p.nombre
HAVING SUM(v.monto) > 30000
ORDER BY total_gastado DESC;