# Taller HPE Private Cloud AI

Los ejercicios utilizan datos ficticios. Para PostgreSQL se requiere una base de pruebas y los permisos correspondientes.

## 1. JupyterLab

Subir estos archivos a una misma carpeta en JupyterLab:

- `01_operaciones_demo.csv`
- `03_notebook_operaciones.ipynb`
- `04_cargar_postgres.py`
- `05_crear_usuario_lectura.py`

Abrir el notebook y seleccionar Run > Run All Cells. El CSV contiene 13 filas, de las cuales 12 son operaciones únicas.

## 2. PostgreSQL

Utilizar una instancia de pruebas existente o importar el framework PostgreSQL desde Tools & Frameworks > Import Framework. El administrador debe confirmar el host, puerto, nombre de la base y credenciales.

[Chart PostgreSQL](https://github.com/ai-solution-eng/frameworks/tree/main/postgresql)

Desde la terminal de JupyterLab, en la carpeta de los archivos:

```bash
python 04_cargar_postgres.py 01_operaciones_demo.csv
```

Si falta el driver y la instalación está permitida:

```bash
python -m pip install psycopg2-binary
```

Introducir los datos de conexión cuando se soliciten. El script crea o actualiza `public.demo_operaciones`.

Opcionalmente, el administrador puede crear un usuario de consulta dedicado:

```bash
python 05_crear_usuario_lectura.py
```

El script crea `workshop_reader` si no existe. Si ya existe, el administrador debe revisar sus permisos y gestionar sus credenciales. Usar una base aislada y comprobar que el usuario no herede permisos de escritura ni acceso a otras tablas. No utilizar el usuario administrador para las consultas del taller.

## 3. EzPresto

1. Ir a Data Engineering > Data Sources > Structured Data > Add New Data Source.
2. Seleccionar PostgreSQL > Create Connection.
3. Name: `workshopdb`.
4. Connection URL: `jdbc:postgresql://<host>:5432/<base>` (ajustar host, puerto y base).
5. Introducir las credenciales del usuario de consulta. Dejar Local Snapshot desactivado inicialmente y seleccionar Connect.
6. En Data Catalog, abrir `workshopdb` > `public` > `demo_operaciones`.
7. En Query Editor, ejecutar las consultas de `05_consultas_ezpresto.sql` una por una.

## 4. Knowledge Base

1. Agregar `02_procedimiento_demo.txt` a una fuente documental compatible con Knowledge Base.
2. Configurar la fuente, los modelos de embeddings e inferencia y el almacenamiento vectorial disponibles en el entorno.
3. Una vez desplegada e indexada la base, abrir Playground y probar las preguntas de `07_preguntas_rag.txt`.
4. Revisar las referencias al documento. Para integraciones externas, consultar RAG Coordinator Endpoint y API Examples.

## 5. MCP con Open WebUI

Se requiere AIE con EzPresto MCP habilitado, Open WebUI 0.6.31 o posterior y un modelo compatible con tool calling.

1. En Data Engineering > Data Sources > Structured Data > MCP Server (Preview), obtener el endpoint y un token autorizado (vigencia de 30 minutos según la versión del taller).
2. En Open WebUI, configurar el endpoint del modelo en Admin Panel > Settings > Connections.
3. En External Tools, agregar un servidor MCP Streamable HTTP con el endpoint y token de EzPresto. Nombre: `PrestoMCP`.
4. En Workspace > Models, crear un modelo basado en el modelo de inferencia configurado. Utilizar `06_prompt_mcp.txt` como System Prompt, habilitar Function Calling: Native y asociar `PrestoMCP`.
5. Abrir un chat, habilitar la herramienta y probar las preguntas de MCP de `07_preguntas_rag.txt`. Comparar los resultados con Query Editor.

Los scripts son para una base de pruebas. Para producción, configurar TLS con validación de certificados, acceso restringido y permisos mínimos. Verificar también la confianza en la CA de PCAI desde Open WebUI y cualquier aplicación externa.
