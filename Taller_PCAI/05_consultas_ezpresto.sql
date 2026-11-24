-- Vista de datos
SELECT * FROM "workshopdb"."public"."demo_operaciones" LIMIT 5;

-- Indicadores por centro
SELECT centro, COUNT(*) AS total,
  SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) AS pendientes,
  ROUND(AVG(tiempo_min), 1) AS promedio_min
FROM "workshopdb"."public"."demo_operaciones"
GROUP BY centro ORDER BY centro;

-- Operaciones mayores a 45 minutos
SELECT id_operacion, centro, tiempo_min
FROM "workshopdb"."public"."demo_operaciones"
WHERE tiempo_min > 45
ORDER BY tiempo_min DESC;
