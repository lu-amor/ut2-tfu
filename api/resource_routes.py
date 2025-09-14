"""
Rutas de API para el sistema de gestión de recursos externos
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from pydantic import BaseModel

def get_router():
    from main import resource_manager
    
    router = APIRouter()

    class ResourceInfo(BaseModel):
        name: str
        value: Any
        type: str

    class ResourceSummary(BaseModel):
        total_resources: int
        resource_directory: str
        watched_files: List[str]
        last_loaded: Dict[str, str]

    @router.get("/", response_model=List[ResourceInfo])
    async def get_all_resources():
        """Obtener todos los recursos cargados"""
        try:
            resources = resource_manager.get_all_resources()
            
            return [
                ResourceInfo(
                    name=name,
                    value=value,
                    type=type(value).__name__
                )
                for name, value in resources.items()
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo recursos: {str(e)}")

    @router.get("/{resource_name}")
    async def get_resource(resource_name: str):
        """Obtener un recurso específico"""
        try:
            resource = resource_manager.get_resource(resource_name)
            if resource is None:
                raise HTTPException(status_code=404, detail=f"Recurso '{resource_name}' no encontrado")
            
            return {
                "name": resource_name,
                "value": resource,
                "type": type(resource).__name__
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo recurso: {str(e)}")

    @router.post("/reload")
    async def reload_all_resources():
        """Recargar todos los recursos desde archivos"""
        try:
            resource_manager.reload_all_resources()
            resource_count = resource_manager.get_resource_count()
            
            return {
                "message": "Todos los recursos han sido recargados",
                "resources_loaded": resource_count
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error recargando recursos: {str(e)}")

    @router.get("/info/summary", response_model=ResourceSummary)
    async def get_resource_summary():
        """Obtener resumen de información sobre recursos"""
        try:
            info = resource_manager.get_resource_info()
            
            return ResourceSummary(
                total_resources=info["total_resources"],
                resource_directory=info["resource_directory"],
                watched_files=info["watched_files"],
                last_loaded=info["last_loaded"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo información: {str(e)}")

    @router.get("/files/list")
    async def list_resource_files():
        """Listar archivos de recursos disponibles"""
        try:
            import os
            resource_dir = resource_manager.resource_dir
            
            if not os.path.exists(resource_dir):
                return {"files": [], "directory": resource_dir}
            
            files = []
            for filename in os.listdir(resource_dir):
                filepath = os.path.join(resource_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    files.append({
                        "name": filename,
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "extension": os.path.splitext(filename)[1]
                    })
            
            return {
                "files": files,
                "directory": resource_dir,
                "total_files": len(files)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listando archivos: {str(e)}")
    
    return router