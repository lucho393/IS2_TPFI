# TPFI - Ingeniería de Software II

Trabajo Práctico Final Integrador de Ingeniería de Software II.

## Descripción

El proyecto implementa un sistema cliente-servidor para consultar y modificar información corporativa almacenada en AWS DynamoDB.

El sistema utiliza las siguientes tablas:

- `CorporateData`: almacena los datos corporativos.
- `CorporateLog`: registra las acciones realizadas sobre el sistema.

La comunicación entre los clientes y el servidor se realiza mediante sockets TCP, intercambiando mensajes en formato JSON.

## Patrones de diseño

El proyecto implementa los siguientes patrones:

- **Singleton:** garantiza una única instancia de acceso a `CorporateData` y `CorporateLog` dentro del proceso.
- **Proxy:** centraliza las operaciones sobre los datos y su correspondiente registro de auditoría.
- **Observer:** permite que los clientes suscriptos reciban notificaciones cuando se modifica `CorporateData`.

## Programas principales

### SingletonClient

Permite realizar las acciones `get`, `set` y `list`.

Ejemplos:

GET:

```bash
python src/singletonclient.py -i input_get.json -o output_get.json
```

SET:

```bash
python src/singletonclient.py -i input_set.json -o output_set.json
```

LIST:

```bash
python src/singletonclient.py -i input_list.json -o output_list.json
```

El parámetro `-i` indica el archivo JSON de entrada y `-o` indica el archivo de salida.

### ObserverClient

Se suscribe al servidor para recibir notificaciones de las modificaciones realizadas sobre `CorporateData`.

Ejemplo:

```bash
python src/observerclient.py -v -o output_observer.json
```

El tiempo de reconexión es de 30 segundos por defecto y puede modificarse mediante el parámetro `--retry`.

### SingletonProxyObserver

Es el servidor principal encargado de recibir y procesar las solicitudes.

Ejemplo:

```bash
python src/singletonproxyobserver.py -v
```

El puerto por defecto es `8080` y puede modificarse mediante el parámetro `--port`.

El parámetro `-v` permite visualizar mensajes de depuración.

## Instalación

Crear el entorno virtual:

```bash
python -m venv venv
```

Activarlo en Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración de AWS

El proyecto utiliza AWS DynamoDB mediante la biblioteca `boto3`.

Para su funcionamiento se requiere:

- Tener AWS CLI configurado con credenciales válidas.
- Contar con permisos para acceder a DynamoDB.
- Tener disponibles las tablas `CorporateData` y `CorporateLog`.
- Utilizar la región de AWS correspondiente a las tablas.

Para verificar la configuración:

```bash
aws configure list
```

Para comprobar que las tablas están disponibles:

```bash
aws dynamodb list-tables --region us-east-1
```

## Ejecución del sistema

Primero se inicia el servidor:

```bash
python src/singletonproxyobserver.py -v
```

En otra terminal se ejecuta SingletonClient con el archivo JSON correspondiente a la operación deseada.

Para recibir notificaciones, se ejecuta ObserverClient en otra terminal:

```bash
python src/observerclient.py -v -o output_observer.json
```

El servidor debe permanecer en ejecución mientras los clientes realizan las solicitudes.

## Pruebas

Las pruebas automatizadas se ejecutan mediante:

```bash
python -m pytest tests --cov=src --cov-report=term-missing
```

El proyecto requiere una cobertura mínima del 85 %.

Las pruebas incluyen verificaciones de los patrones Singleton, Proxy y Observer, las operaciones del servidor, el comportamiento de los clientes y distintos escenarios de error.

Las pruebas unitarias utilizan simulaciones para verificar el comportamiento del código sin modificar las tablas reales de AWS.

## Calidad del código

Para verificar la calidad y seguridad del código se utilizan las siguientes herramientas:

**Ruff:**

```bash
python -m ruff check src tests
```

**Black:**

```bash
python -m black --check src tests
```

**PEP8:**

```bash
python -m pycodestyle src tests
```

**PEP257:**

```bash
python -m pydocstyle src
```

**MyPy:**

```bash
python -m mypy src
```

**PyRight:**

```bash
python -m pyright src
```

**Bandit:**

```bash
python -m bandit -r src
```

## Documentación

La documentación de los módulos Python fue generada mediante `pdoc` y se encuentra en la carpeta `docs/`.

Para consultarla, abrir el archivo:

```text
docs/index.html
```

## Versión

Versión: `1.0.0`

Build: `1`

Los cambios realizados en el proyecto se registran en el archivo `CHANGELOG.md`.

## Licencia

Este proyecto utiliza la licencia MIT. Consultar el archivo `LICENSE`.