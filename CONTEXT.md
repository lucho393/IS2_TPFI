# Contexto de uso de Inteligencia Artificial

## 1. Introducción

Durante el desarrollo del Trabajo Práctico Final Integrador de Ingeniería de Software II se utilizó ChatGPT como herramienta de apoyo para interpretar los requisitos, organizar el proyecto, comprender e implementar los patrones de diseño, resolver errores y preparar las pruebas.

Las consultas se realizaron de manera progresiva, a medida que avanzaba el desarrollo. El código fue ejecutado y revisado en el entorno local del proyecto.

A continuación se documentan los principales prompts utilizados, redactados de forma representativa. No constituyen una transcripción literal de todas las conversaciones.

## 2. Prompts utilizados

### 2.1. Análisis de la consigna

**Objetivo:** identificar las funcionalidades obligatorias y los requisitos técnicos del TPFI.

**Prompt:**

> Analizá la consigna del TPFI de Ingeniería de Software II y explicame qué debemos implementar. Identificá los programas, patrones de diseño, operaciones, pruebas y requisitos obligatorios, sin agregar funcionalidades que no solicite el profesor.

### 2.2. Organización del proyecto con CookieCutter

**Objetivo:** preparar la estructura inicial del proyecto.

**Prompt:**

> Ayudame a organizar el proyecto utilizando CookieCutter y un entorno virtual de Python. Explicame cómo separar el código fuente, las pruebas, la documentación y los archivos de configuración.

### 2.3. Configuración de AWS DynamoDB

**Objetivo:** establecer y verificar la conexión con las tablas utilizadas por el sistema.

**Prompt:**

> Explicame cómo configurar boto3 y AWS CLI para conectarme a DynamoDB en la región us-east-1 y verificar el acceso a las tablas CorporateData y CorporateLog.

### 2.4. Implementación del patrón Singleton

**Objetivo:** centralizar el acceso a las tablas DynamoDB.

**Prompt:**

> Ayudame a implementar el patrón Singleton en Python para acceder a las tablas CorporateData y CorporateLog mediante boto3. Explicame cómo funciona el método **new** y cómo comprobar que se utiliza una única instancia de cada clase.

### 2.5. Implementación del patrón Proxy

**Objetivo:** intermediar las operaciones sobre los datos y registrar las acciones.

**Prompt:**

> Ayudame a implementar CorporateDataProxy para realizar las operaciones get, set y list, utilizando los Singleton de CorporateData y CorporateLog. Explicame cómo se relacionan las clases y cómo se registra la auditoría.

### 2.6. Implementación del patrón Observer

**Objetivo:** permitir que los clientes suscriptos reciban notificaciones.

**Prompt:**

> Ayudame a implementar el patrón Observer para registrar clientes suscriptos mediante sockets TCP y notificarles cuando se modifica un registro de CorporateData.&#x20;

### 2.7. Desarrollo del servidor y los clientes

**Objetivo:** implementar la comunicación cliente-servidor solicitada.

**Prompt:**

> Ayudame a desarrollar singletonclient.py, observerclient.py y singletonproxyobserver.py utilizando Python, sockets TCP y mensajes JSON. El servidor debe procesar GET, SET, LIST y SUBSCRIBE respetando los argumentos establecidos en la consigna.

### 2.8. Resolución de errores

**Objetivo:** identificar y corregir problemas durante la ejecución.

**Prompts:**

> Al ejecutar el proyecto aparece un error ResourceNotFoundException de DynamoDB. Ayudame a identificar si está relacionado con la región AWS o con las tablas configuradas.

> Tengo errores ModuleNotFoundError e ImportError al ejecutar los módulos Python. Explicame cómo revisar las importaciones y la estructura del proyecto.

> Aparece un error WinError 10038 relacionado con sockets. Ayudame a comprender la causa y revisar el manejo de conexiones.

### 2.9. Pruebas automatizadas

**Objetivo:** verificar el funcionamiento de los componentes y patrones implementados.

**Prompt:**

> Ayudame a desarrollar pruebas automatizadas con pytest para verificar Singleton, Proxy y Observer. También necesito comprobar las operaciones correctas, argumentos inválidos, datos faltantes y errores de conexión establecidos en la consigna.

### 2.10. Cobertura de pruebas

**Objetivo:** analizar la cobertura y detectar partes del código que necesitan más pruebas.

**Prompt:**

> Explicame cómo ejecutar pytest con pytest-cov, interpretar los resultados de cobertura y determinar qué funciones necesitan pruebas adicionales para alcanzar el mínimo del 85 % exigido por el profesor.

### 2.11. Calidad y seguridad del código

**Objetivo:** comprobar el cumplimiento de los requisitos técnicos.

**Prompt:**

> Ayudame a revisar el proyecto utilizando Ruff, Black, pycodestyle, pydocstyle, MyPy, PyRight y Bandit. Explicame cómo ejecutar cada herramienta, interpretar sus resultados y corregir los problemas detectados sin modificar las funcionalidades requeridas.

### 2.12. Documentación del proyecto

**Objetivo:** preparar los archivos de documentación solicitados.

**Prompt:**

> Ayudame a organizar README.md, CHANGELOG.md, CONTEXT.md, VERSION, BUILD y la documentación automática del proyecto, respetando los requisitos establecidos por el profesor.

### 2.13. Revisión de cumplimiento

**Objetivo:** comparar el desarrollo realizado con la consigna original.

**Prompt:**

> Revisemos punto por punto la consigna del TPFI y comparemos cada requisito con los archivos del proyecto. Indicame si está implementado, dónde se encuentra, cómo funciona y qué falta completar para la entrega.

## 3. Alcance de la utilización de IA

La inteligencia artificial se utilizó como apoyo para comprender conceptos, proponer implementaciones, analizar errores, preparar pruebas y organizar la documentación.

La utilización de esta herramienta no reemplaza la ejecución de los programas ni la verificación de los resultados.&#x20;
