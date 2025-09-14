"""
Rutas de API para el sistema de reemplazo de componentes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

def get_router():
    from main import component_registry
    
    router = APIRouter()

    class ComponentInfo(BaseModel):
        name: str
        state: str
        start_time: Optional[str] = None
        error_message: Optional[str] = None
        class_name: str

    class ComponentHealth(BaseModel):
        component_name: str
        healthy: bool

    @router.get("/", response_model=List[ComponentInfo])
    async def list_components():
        """Listar todos los componentes registrados"""
        try:
            components = component_registry.list_components()
            
            return [
                ComponentInfo(
                    name=name,
                    state=info["state"],
                    start_time=info["start_time"],
                    error_message=info["error_message"],
                    class_name=info["class"]
                )
                for name, info in components.items()
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listando componentes: {str(e)}")

    @router.get("/types")
    async def list_component_types():
        """Listar tipos de componentes disponibles"""
        try:
            types = component_registry.list_component_types()
            return {
                "available_types": types,
                "total_types": len(types)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listando tipos: {str(e)}")

    @router.post("/{component_name}/start")
    async def start_component(component_name: str):
        """Iniciar un componente"""
        try:
            success = await component_registry.start_component(component_name)
            if not success:
                raise HTTPException(status_code=400, detail=f"No se pudo iniciar el componente '{component_name}'")
            
            return {
                "message": f"Componente '{component_name}' iniciado exitosamente",
                "component_name": component_name,
                "action": "start"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error iniciando componente: {str(e)}")

    @router.post("/{component_name}/stop")
    async def stop_component(component_name: str):
        """Detener un componente"""
        try:
            success = await component_registry.stop_component(component_name)
            if not success:
                raise HTTPException(status_code=400, detail=f"No se pudo detener el componente '{component_name}'")
            
            return {
                "message": f"Componente '{component_name}' detenido exitosamente",
                "component_name": component_name,
                "action": "stop"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deteniendo componente: {str(e)}")

    @router.post("/create")
    async def create_component(component_type: str, instance_name: str):
        """Crear una nueva instancia de componente"""
        try:
            success = component_registry.create_component(component_type, instance_name)
            if not success:
                raise HTTPException(status_code=400, detail=f"No se pudo crear el componente '{instance_name}' del tipo '{component_type}'")
            
            return {
                "message": f"Componente '{instance_name}' del tipo '{component_type}' creado exitosamente",
                "component_name": instance_name,
                "component_type": component_type,
                "action": "create"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creando componente: {str(e)}")

    @router.put("/{component_name}/replace")
    async def replace_component(component_name: str, new_component_type: str):
        """Reemplazar un componente existente con uno de diferente tipo"""
        try:
            success = component_registry.replace_component(component_name, new_component_type)
            if not success:
                raise HTTPException(status_code=400, detail=f"No se pudo reemplazar el componente '{component_name}' con tipo '{new_component_type}'")
            
            return {
                "message": f"Componente '{component_name}' reemplazado exitosamente con tipo '{new_component_type}'",
                "component_name": component_name,
                "new_type": new_component_type,
                "action": "replace"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reemplazando componente: {str(e)}")

    @router.get("/health/all", response_model=List[ComponentHealth])
    async def health_check_all():
        """Verificar la salud de todos los componentes"""
        try:
            health_results = await component_registry.health_check_all()
            
            return [
                ComponentHealth(
                    component_name=name,
                    healthy=healthy
                )
                for name, healthy in health_results.items()
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error verificando salud: {str(e)}")
    
    return router