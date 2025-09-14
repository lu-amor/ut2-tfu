"""
Sistema de monitoreo de condiciones
Verifica durante la ejecución que ciertas condiciones específicas se cumplan
Genera alertas cuando se detectan anomalías
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class Alert:
    id: str
    level: AlertLevel
    message: str
    timestamp: datetime
    condition_name: str
    current_value: Any
    expected_range: str

@dataclass
class Condition:
    name: str
    description: str
    check_function: Callable[[], Any]
    validator: Callable[[Any], bool]
    alert_level: AlertLevel
    check_interval: float = 5.0  # segundos
    enabled: bool = True

class ConditionMonitor:
    def __init__(self):
        self.conditions: Dict[str, Condition] = {}
        self.alerts: List[Alert] = []
        self.running = False
        self.tasks = []
        
    def add_condition(self, condition: Condition):
        """Agregar una nueva condición a monitorear"""
        self.conditions[condition.name] = condition
        
    def remove_condition(self, condition_name: str):
        """Remover una condición del monitoreo"""
        if condition_name in self.conditions:
            del self.conditions[condition_name]
            
    def enable_condition(self, condition_name: str, enabled: bool = True):
        """Habilitar/deshabilitar una condición"""
        if condition_name in self.conditions:
            self.conditions[condition_name].enabled = enabled
            
    async def check_condition(self, condition: Condition):
        """Verificar una condición específica"""
        try:
            current_value = condition.check_function()
            is_valid = condition.validator(current_value)
            
            if not is_valid:
                alert = Alert(
                    id=f"alert_{condition.name}_{int(time.time())}",
                    level=condition.alert_level,
                    message=f"Condición '{condition.name}' falló: {condition.description}",
                    timestamp=datetime.now(),
                    condition_name=condition.name,
                    current_value=current_value,
                    expected_range="Según validador configurado"
                )
                self.alerts.append(alert)
                print(f"[{alert.timestamp}] ALERTA {alert.level.value.upper()}: {alert.message}")
                
        except Exception as e:
            alert = Alert(
                id=f"error_{condition.name}_{int(time.time())}",
                level=AlertLevel.ERROR,
                message=f"Error verificando condición '{condition.name}': {str(e)}",
                timestamp=datetime.now(),
                condition_name=condition.name,
                current_value="ERROR",
                expected_range="N/A"
            )
            self.alerts.append(alert)
            
    async def monitor_loop(self, condition: Condition):
        """Loop de monitoreo para una condición específica"""
        while self.running:
            if condition.enabled and condition.name in self.conditions:
                await self.check_condition(condition)
            await asyncio.sleep(condition.check_interval)
            
    async def start(self):
        """Iniciar el sistema de monitoreo"""
        self.running = True
        # Iniciar condiciones de ejemplo
        self._setup_default_conditions()
        
        # Crear tareas de monitoreo para cada condición
        for condition in self.conditions.values():
            task = asyncio.create_task(self.monitor_loop(condition))
            self.tasks.append(task)
            
    async def stop(self):
        """Detener el sistema de monitoreo"""
        self.running = False
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        
    def is_running(self) -> bool:
        """Verificar si el sistema está ejecutándose"""
        return self.running
        
    def get_alerts(self, level: AlertLevel = None, limit: int = 100) -> List[Alert]:
        """Obtener alertas filtradas"""
        alerts = self.alerts
        if level:
            alerts = [a for a in alerts if a.level == level]
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)[:limit]
        
    def get_conditions(self) -> Dict[str, dict]:
        """Obtener estado de todas las condiciones"""
        return {
            name: {
                "description": condition.description,
                "enabled": condition.enabled,
                "alert_level": condition.alert_level.value,
                "check_interval": condition.check_interval
            }
            for name, condition in self.conditions.items()
        }
        
    def clear_alerts(self):
        """Limpiar todas las alertas"""
        self.alerts.clear()
        
    def _setup_default_conditions(self):
        """Configurar condiciones de ejemplo para la demo"""
        import psutil
        import random
        
        # Condición 1: Uso de CPU
        cpu_condition = Condition(
            name="cpu_usage",
            description="Uso de CPU debe estar por debajo del 80%",
            check_function=lambda: psutil.cpu_percent(interval=1),
            validator=lambda x: x < 80,
            alert_level=AlertLevel.WARNING,
            check_interval=10.0
        )
        
        # Condición 2: Memoria disponible
        memory_condition = Condition(
            name="memory_available",
            description="Memoria disponible debe ser mayor a 100MB",
            check_function=lambda: psutil.virtual_memory().available / 1024 / 1024,
            validator=lambda x: x > 100,
            alert_level=AlertLevel.ERROR,
            check_interval=15.0
        )
        
        # Condición 3: Simulación de temperatura
        temp_condition = Condition(
            name="temperature_sensor",
            description="Temperatura del sensor debe estar entre 20-80°C",
            check_function=lambda: random.uniform(15, 85),  # Simulación
            validator=lambda x: 20 <= x <= 80,
            alert_level=AlertLevel.CRITICAL,
            check_interval=5.0
        )
        
        # Condición 4: Conectividad de red
        network_condition = Condition(
            name="network_connectivity",
            description="Debe haber actividad de red",
            check_function=lambda: psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
            validator=lambda x: x > 0,
            alert_level=AlertLevel.WARNING,
            check_interval=20.0
        )
        
        self.add_condition(cpu_condition)
        self.add_condition(memory_condition)
        self.add_condition(temp_condition)
        self.add_condition(network_condition)