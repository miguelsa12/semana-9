"""Crea un usuario de consulta para la base de pruebas."""
import getpass

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    raise SystemExit('Falta el driver: python -m pip install psycopg2-binary')

if input('Escribe DEMO para confirmar que es una base de pruebas: ').strip() != 'DEMO':
    raise SystemExit('Cancelado.')

host = input('Host: ').strip()
port = input('Puerto [5432]: ').strip() or '5432'
db = input('Base de datos de prueba: ').strip()
admin = input('Usuario administrador: ').strip()
admin_password = getpass.getpass('Contraseña del administrador: ')
if not all([host, db, admin, admin_password]):
    raise SystemExit('Faltan datos de conexión.')

new_password = getpass.getpass('Nueva contraseña para workshop_reader (mínimo 16 caracteres): ')
confirmation = getpass.getpass('Repite la contraseña: ')
if len(new_password) < 16 or new_password != confirmation:
    raise SystemExit('Las contraseñas no coinciden o son demasiado cortas.')

connection = dict(host=host, port=port, dbname=db, connect_timeout=10, sslmode='prefer')
with psycopg2.connect(**connection, user=admin, password=admin_password) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', ('workshop_reader',))
        if cur.fetchone():
            raise SystemExit('workshop_reader ya existe. Solicita al administrador revisar el usuario existente.')
        cur.execute('CREATE ROLE workshop_reader LOGIN PASSWORD %s', (new_password,))
        cur.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO workshop_reader').format(sql.Identifier(db)))
        cur.execute('GRANT USAGE ON SCHEMA public TO workshop_reader')
        cur.execute('GRANT SELECT ON TABLE public.demo_operaciones TO workshop_reader')

with psycopg2.connect(**connection, user='workshop_reader', password=new_password) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM public.demo_operaciones')
        print('Filas visibles:', cur.fetchone()[0])
