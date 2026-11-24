"""Carga los datos del taller en PostgreSQL (solo pruebas)."""
import csv
import getpass
import sys
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    raise SystemExit('Falta el driver: python -m pip install psycopg2-binary')

path = Path(sys.argv[1] if len(sys.argv) > 1 else '01_operaciones_demo.csv')
if not path.exists():
    raise SystemExit(f'No encuentro {path} en esta carpeta.')

print('Base de pruebas: se crea o actualiza public.demo_operaciones.')
if input('Escribe DEMO para continuar: ').strip() != 'DEMO':
    raise SystemExit('Cancelado.')
host = input('Host: ').strip()
port = input('Puerto [5432]: ').strip() or '5432'
db = input('Base de datos de prueba: ').strip()
user = input('Usuario: ').strip()
password = getpass.getpass('Contraseña: ')
if not all([host, db, user, password]):
    raise SystemExit('Faltan datos de conexión.')

with path.open(encoding='utf-8-sig', newline='') as f:
    raw = list(csv.DictReader(f))
dedup = {}
for r in raw:
    dedup.setdefault(r['id_operacion'], r)
values = [
    (r['id_operacion'], r['fecha'], r['centro'], r['estado'],
     float(r['tiempo_min']) if r['tiempo_min'].strip() else None)
    for r in dedup.values()
]

with psycopg2.connect(host=host, port=port, dbname=db, user=user,
                      password=password, connect_timeout=10, sslmode='prefer') as conn:
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS public.demo_operaciones (
                id_operacion TEXT PRIMARY KEY,
                fecha DATE NOT NULL,
                centro TEXT NOT NULL,
                estado TEXT NOT NULL,
                tiempo_min DOUBLE PRECISION
            )
        ''')
        execute_values(cur, '''
            INSERT INTO public.demo_operaciones
                (id_operacion, fecha, centro, estado, tiempo_min)
            VALUES %s
            ON CONFLICT (id_operacion) DO UPDATE SET
                fecha = EXCLUDED.fecha,
                centro = EXCLUDED.centro,
                estado = EXCLUDED.estado,
                tiempo_min = EXCLUDED.tiempo_min
        ''', values)
        cur.execute('SELECT COUNT(*) FROM public.demo_operaciones')
        print('Filas actuales en la tabla:', cur.fetchone()[0])
        cur.execute('''SELECT centro, COUNT(*),
            SUM(CASE WHEN estado='Pendiente' THEN 1 ELSE 0 END)
            FROM public.demo_operaciones GROUP BY centro ORDER BY centro''')
        print('Centro | Total | Pendientes')
        for row in cur.fetchall():
            print(row)
print('Carga de prueba finalizada.')
