"""
Rutas de API para el sistema de monitoreo de condiciones
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from monitoring.condition_monitor import AlertLevel

def get_router():
    from main import condition_monitor
    
    router = APIRouter()

    class AlertResponse(BaseModel):
        id: str
        level: str
        message: str
        timestamp: str
        condition_name: str
        current_value: str
        expected_range: str

    class ConditionInfo(BaseModel):
        name: str
        description: str
        enabled: bool
        alert_level: str
        check_interval: float

    @router.get("/alerts", response_model=List[AlertResponse])
    async def get_alerts(
        level: Optional[str] = Query(None, description="Filtrar por nivel de alerta"),
        limit: int = Query(100, description="Límite de alertas a retornar")
    ):
        """Obtener alertas del sistema de monitoreo"""
        try:
            alert_level = None
            if level:
                alert_level = AlertLevel(level.lower())
            
            alerts = condition_monitor.get_alerts(alert_level, limit)
            
            return [
                AlertResponse(
                    id=alert.id,
                    level=alert.level.value,
                    message=alert.message,
                    timestamp=alert.timestamp.isoformat(),
                    condition_name=alert.condition_name,
                    current_value=str(alert.current_value),
                    expected_range=alert.expected_range
                )
                for alert in alerts
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo alertas: {str(e)}")

    @router.get("/conditions", response_model=List[ConditionInfo])
    async def get_conditions():
        """Obtener estado de todas las condiciones monitoreadas"""
        try:
            conditions = condition_monitor.get_conditions()
            
            return [
                ConditionInfo(
                    name=name,
                    description=info["description"],
                    enabled=info["enabled"],
                    alert_level=info["alert_level"],
                    check_interval=info["check_interval"]
                )
                for name, info in conditions.items()
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo condiciones: {str(e)}")

    @router.post("/conditions/{condition_name}/enable")
    async def enable_condition(condition_name: str, enabled: bool = True):
        """Habilitar o deshabilitar una condición específica"""
        try:
            condition_monitor.enable_condition(condition_name, enabled)
            return {
                "message": f"Condición '{condition_name}' {'habilitada' if enabled else 'deshabilitada'}",
                "condition_name": condition_name,
                "enabled": enabled
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error modificando condición: {str(e)}")

    @router.delete("/alerts")
    async def clear_alerts():
        """Limpiar todas las alertas"""
        try:
            condition_monitor.clear_alerts()
            return {"message": "Todas las alertas han sido eliminadas"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error limpiando alertas: {str(e)}")

    @router.get("/status")
    async def get_monitoring_status():
        """Obtener estado del sistema de monitoreo"""
        try:
            conditions = condition_monitor.get_conditions()
            alerts = condition_monitor.get_alerts(limit=10)
            
            return {
                "is_running": condition_monitor.is_running(),
                "total_conditions": len(conditions),
                "enabled_conditions": len([c for c in conditions.values() if c["enabled"]]),
                "total_alerts": len(condition_monitor.alerts),
                "recent_alerts": len(alerts),
                "alert_levels": {
                    level.value: len([a for a in alerts if a.level == level])
                    for level in AlertLevel
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")

    @router.post("/test-alert")
    async def create_test_alert():
        """Crear una alerta de prueba para testing"""
        try:
            from monitoring.condition_monitor import Alert, AlertLevel
            from datetime import datetime
            
            test_alert = Alert(
                id=f"test_alert_{int(datetime.now().timestamp())}",
                level=AlertLevel.WARNING,
                message="Esta es una alerta de prueba generada manualmente",
                timestamp=datetime.now(),
                condition_name="test_condition",
                current_value="test_value",
                expected_range="test_range"
            )
            
            condition_monitor.alerts.append(test_alert)
            
            return {
                "message": "Alerta de prueba creada exitosamente",
                "alert_id": test_alert.id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creando alerta de prueba: {str(e)}")
    
    return router