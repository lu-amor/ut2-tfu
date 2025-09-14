# Sistema de Monitoreo y Gestión de Componentes

API Python para demostrar tres características principales del desarrollo de software empresarial:

## 🎯 Características Principales

### 1. 🔍 Monitoreo de Condiciones
Sistema de verificación continua que monitora condiciones específicas de operación durante la ejecución:
- Verificación automática de métricas del sistema (CPU, memoria, temperatura)
- Generación automática de alertas cuando se detectan anomalías
- Configuración de umbrales y niveles de alerta
- Habilitación/deshabilitación dinámica de condiciones

### 2. 📄 Archivos de Recursos Externos
Gestión de recursos almacenados en archivos externos para facilitar modificaciones sin recompilación:
- Carga automática de configuraciones desde archivos JSON/YAML
- Monitoreo de cambios en archivos con recarga automática
- Acceso dinámico a recursos en tiempo de ejecución
- Separación entre código y configuración

### 3. 🔄 Reemplazo de Componentes
Sistema diseñado para permitir el reemplazo dinámico de componentes:
- Registro de tipos de componentes disponibles
- Creación y eliminación de instancias en tiempo de ejecución
- Reemplazo de componentes sin reiniciar el sistema
- Verificación de salud de componentes

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- pip

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/lu-amor/ut2-tfu.git
cd ut2-tfu

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python main.py
```

El servidor estará disponible en: http://localhost:8000

### Documentación API
Una vez ejecutándose, visite: http://localhost:8000/docs para la documentación interactiva de la API.

## 🎮 Demostración

Ejecute el script de demostración para ver todas las características en acción:

```bash
python demo.py
```

Este script demostrará:
- Monitoreo activo de condiciones del sistema
- Carga y gestión de recursos externos
- Operaciones de componentes (crear, iniciar, reemplazar)

## 📚 Estructura del Proyecto

```
ut2-tfu/
├── main.py                    # Aplicación principal FastAPI
├── requirements.txt           # Dependencias
├── demo.py                   # Script de demostración
├── monitoring/               # Sistema de monitoreo
│   ├── __init__.py
│   └── condition_monitor.py  # Monitor de condiciones
├── resources/                # Gestión de recursos
│   ├── __init__.py
│   └── resource_manager.py   # Gestor de recursos
├── components/               # Sistema de componentes
│   ├── __init__.py
│   └── component_registry.py # Registro de componentes
├── api/                      # Endpoints de la API
│   ├── __init__.py
│   ├── monitoring_routes.py  # Rutas de monitoreo
│   ├── resource_routes.py    # Rutas de recursos
│   └── component_routes.py   # Rutas de componentes
└── config/                   # Archivos de configuración
    └── resources/            # Recursos externos
        ├── app_config.json
        ├── monitoring_thresholds.yaml
        ├── alert_messages.json
        └── component_config.yaml
```

## 🔌 Endpoints de la API

### Monitoreo (`/api/monitoring`)
- `GET /alerts` - Obtener alertas del sistema
- `GET /conditions` - Listar condiciones monitoreadas
- `POST /conditions/{name}/enable` - Habilitar/deshabilitar condición
- `GET /status` - Estado del sistema de monitoreo
- `POST /test-alert` - Crear alerta de prueba
- `DELETE /alerts` - Limpiar todas las alertas

### Recursos (`/api/resources`)
- `GET /` - Listar todos los recursos cargados
- `GET /{name}` - Obtener recurso específico
- `POST /reload` - Recargar todos los recursos
- `GET /info/summary` - Resumen del sistema de recursos
- `GET /files/list` - Listar archivos de recursos

### Componentes (`/api/components`)
- `GET /` - Listar componentes registrados
- `GET /types` - Tipos de componentes disponibles
- `POST /{name}/start` - Iniciar componente
- `POST /{name}/stop` - Detener componente
- `POST /create` - Crear nueva instancia
- `PUT /{name}/replace` - Reemplazar componente
- `GET /health/all` - Verificar salud de todos los componentes

## 🔧 Configuración

### Archivos de Recursos
Los archivos de configuración se encuentran en `config/resources/`:

- **app_config.json**: Configuración general de la aplicación
- **monitoring_thresholds.yaml**: Umbrales para el monitoreo
- **alert_messages.json**: Mensajes de alerta personalizados
- **component_config.yaml**: Configuración de componentes

Estos archivos pueden modificarse en tiempo de ejecución y se recargarán automáticamente.

### Condiciones de Monitoreo por Defecto
El sistema incluye condiciones de monitoreo predefinidas:
- **CPU Usage**: Verifica que el uso de CPU sea menor al 80%
- **Memory Available**: Verifica memoria disponible mayor a 100MB
- **Temperature Sensor**: Simula sensor de temperatura (20-80°C)
- **Network Connectivity**: Verifica actividad de red

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno para Python
- **Uvicorn**: Servidor ASGI para aplicaciones FastAPI
- **Pydantic**: Validación de datos y configuración
- **PyYAML**: Procesamiento de archivos YAML
- **Watchdog**: Monitoreo de cambios en archivos
- **psutil**: Información del sistema y procesos

## 🎯 Casos de Uso

### Monitoreo de Condiciones
- Sistemas de alerta temprana
- Monitoreo de infraestructura
- Verificación de SLA
- Detección de anomalías

### Recursos Externos
- Configuración de aplicaciones empresariales
- Gestión de secretos y credenciales
- Personalización por entorno
- Configuración sin downtime

### Reemplazo de Componentes
- Sistemas de alta disponibilidad
- Actualizaciones en caliente
- A/B testing de componentes
- Arquitectura de microservicios

## 🤝 Contribución

Este proyecto es una demostración educativa. Para contribuir:

1. Fork el proyecto
2. Crear una rama para la característica
3. Hacer commit de los cambios
4. Hacer push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.