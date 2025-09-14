"""
API Principal para demostrar:
- Monitoreo de condiciones
- Archivos de recursos externos
- Reemplazo de componentes
"""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn
from monitoring.condition_monitor import ConditionMonitor
from resources.resource_manager import ResourceManager
from components.component_registry import ComponentRegistry

# Inicializar sistemas globales
condition_monitor = ConditionMonitor()
resource_manager = ResourceManager()
component_registry = ComponentRegistry()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Inicialización
    await condition_monitor.start()
    resource_manager.load_resources()
    component_registry.load_components()
    
    yield
    
    # Limpieza
    await condition_monitor.stop()

app = FastAPI(
    title="Sistema de Monitoreo y Gestión de Componentes",
    description="API para demostrar monitoreo de condiciones, recursos externos y reemplazo de componentes",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "API de Demo - Sistema de Monitoreo y Gestión de Componentes",
        "endpoints": {
            "monitoring": "/api/monitoring",
            "resources": "/api/resources", 
            "components": "/api/components",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "monitoring": condition_monitor.is_running(),
        "resources_loaded": resource_manager.get_resource_count(),
        "components_loaded": component_registry.get_component_count()
    }

# Importar e incluir rutas después de definir el app
from api.monitoring_routes import get_router as get_monitoring_router
from api.resource_routes import get_router as get_resource_router
from api.component_routes import get_router as get_component_router

app.include_router(get_monitoring_router(), prefix="/api/monitoring", tags=["monitoring"])
app.include_router(get_resource_router(), prefix="/api/resources", tags=["resources"])
app.include_router(get_component_router(), prefix="/api/components", tags=["components"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)