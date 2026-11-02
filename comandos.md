Iniciar servidor — Terminal 1
Inicia el servidor TCP en el puerto 8080 y muestra mensajes detallados.
python src/singletonproxyobserver.py

Camino feliz — Terminal 2
GET: consulta un registro existente y guarda la respuesta en un archivo JSON.
python src/singletonclient.py -i input_get.json -o output_get.json -v

LIST: obtiene los registros disponibles en CorporateData y guarda la respuesta.
python src/singletonclient.py -i input_list.json -o output_list.json -v

SET: crea o modifica un registro, registra la operación y puede generar notificaciones.
python src/singletonclient.py -i input_set.json -o output_set.json -v
Observer — Terminales 3 y 2

Observer (terminal 3): se suscribe al servidor y espera notificaciones de cambios.
python src/observerclient.py -o output_observer.json -v

SET (terminal 2): modifica un registro para provocar una notificación al Observer suscripto.
python src/singletonclient.py -i input_set.json -o output_set.json -v

Pruebas de error
GET inválido: envía una solicitud con datos obligatorios faltantes para verificar la validación.
python src/singletonclient.py -i input_get_invalido.json -v

GET inexistente: solicita un registro que no existe y comprueba la respuesta de error.
python src/singletonclient.py -i input_get_inexistente.json -v

SET inválido: envía una solicitud de modificación incompleta y verifica su rechazo.
python src/singletonclient.py -i input_set_invalido.json -v

Puerto ocupado: con el primer servidor encendido, intenta iniciar otro en el mismo puerto.
python src/singletonproxyobserver.py -v

Servidor apagado: después de detener el servidor con Ctrl+C, intenta conectar el cliente y observa el error de conexión.
python src/singletonclient.py -i input_get.json -v

Pruebas automatizadas
Ejecuta Pytest y muestra el porcentaje de cobertura y las líneas no cubiertas.
python -m pytest tests --cov=src --cov-report=term-missing

Calidad y seguridad
Ruff: detecta problemas de estilo y posibles errores en el código.
python -m ruff check src tests

Black: comprueba el formato del código sin modificar los archivos.
python -m black --check src tests

Pycodestyle: comprueba las convenciones de estilo de Python configuradas.
python -m pycodestyle --max-line-length=88 src tests

Pydocstyle: comprueba las convenciones de documentación de los docstrings.
python -m pydocstyle src

MyPy: analiza posibles problemas de tipos en el código fuente.
python -m mypy src

PyRight: realiza un análisis estático adicional de tipos.
python -m pyright src

Bandit: analiza posibles riesgos de seguridad en el código fuente.
python -m bandit -r src
