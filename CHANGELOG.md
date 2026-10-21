# Changelog

## 1.0.0

- Creación inicial del proyecto mediante CookieCutter.
- Configuración de la estructura base del TPFI.
- Implementación del acceso a `CorporateData` mediante el patrón Singleton.
- Implementación del acceso a `CorporateLog` mediante el patrón Singleton.
- Implementación del patrón Proxy para gestionar el acceso a los datos y el registro de auditoría.
- Implementación del patrón Observer para gestionar clientes suscriptos.
- Implementación del servidor `SingletonProxyObserver`.
- Implementación del cliente `SingletonClient`.
- Implementación del cliente `ObserverClient`.
- Implementación de las acciones `get`, `set`, `list` y `subscribe`.
- Incorporación del registro de acciones en `CorporateLog`.
- Incorporación de reconexión parametrizable en `ObserverClient`, con 30 segundos por defecto.
- Incorporación de paginación para recuperar el contenido completo de `CorporateData`.
- Implementación de pruebas automatizadas.
- Verificación de cobertura de pruebas superior al 85 %.
- Incorporación de controles de calidad mediante Black, Ruff, pycodestyle, pydocstyle, MyPy y PyRight.
- Verificación de seguridad mediante Bandit.