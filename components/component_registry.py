"""
Sistema de reemplazo de componentes
Diseñado para que los componentes puedan ser reemplazados dinámicamente
"""

import importlib
import inspect
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, List
from datetime import datetime
from enum import Enum

class ComponentState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"

class BaseComponent(ABC):
    """Clase base para todos los componentes del sistema"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = ComponentState.STOPPED
        self.start_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        
    @abstractmethod
    async def start(self) -> bool:
        """Iniciar el componente"""
        pass
        
    @abstractmethod
    async def stop(self) -> bool:
        """Detener el componente"""
        pass
        
    @abstractmethod
    async def health_check(self) -> bool:
        """Verificar la salud del componente"""
        pass
        
    def get_info(self) -> Dict[str, Any]:
        """Obtener información del componente"""
        return {
            "name": self.name,
            "state": self.state.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "error_message": self.error_message,
            "class": self.__class__.__name__
        }

class LoggingComponent(BaseComponent):
    """Componente de logging de ejemplo"""
    
    def __init__(self):
        super().__init__("logging")
        self.log_entries: List[Dict] = []
        
    async def start(self) -> bool:
        self.state = ComponentState.STARTING
        try:
            self.start_time = datetime.now()
            self.state = ComponentState.RUNNING
            self.log("Componente de logging iniciado")
            return True
        except Exception as e:
            self.state = ComponentState.ERROR
            self.error_message = str(e)
            return False
            
    async def stop(self) -> bool:
        self.state = ComponentState.STOPPING
        self.log("Componente de logging detenido")
        self.state = ComponentState.STOPPED
        return True
        
    async def health_check(self) -> bool:
        return self.state == ComponentState.RUNNING
        
    def log(self, message: str, level: str = "INFO"):
        """Agregar entrada de log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.log_entries.append(entry)
        print(f"[{entry['timestamp']}] {level}: {message}")
        
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Obtener entradas de log"""
        return self.log_entries[-limit:]

class AlertingComponent(BaseComponent):
    """Componente de alertas de ejemplo"""
    
    def __init__(self):
        super().__init__("alerting")
        self.alert_count = 0
        
    async def start(self) -> bool:
        self.state = ComponentState.STARTING
        try:
            self.start_time = datetime.now()
            self.state = ComponentState.RUNNING
            return True
        except Exception as e:
            self.state = ComponentState.ERROR
            self.error_message = str(e)
            return False
            
    async def stop(self) -> bool:
        self.state = ComponentState.STOPPING
        self.state = ComponentState.STOPPED
        return True
        
    async def health_check(self) -> bool:
        return self.state == ComponentState.RUNNING
        
    def send_alert(self, message: str, level: str = "INFO"):
        """Enviar alerta"""
        self.alert_count += 1
        print(f"ALERTA [{level}]: {message}")

class MonitoringComponent(BaseComponent):
    """Componente de monitoreo de ejemplo"""
    
    def __init__(self):
        super().__init__("monitoring")
        self.monitored_metrics = {}
        
    async def start(self) -> bool:
        self.state = ComponentState.STARTING
        try:
            self.start_time = datetime.now()
            self.state = ComponentState.RUNNING
            return True
        except Exception as e:
            self.state = ComponentState.ERROR
            self.error_message = str(e)
            return False
            
    async def stop(self) -> bool:
        self.state = ComponentState.STOPPING
        self.state = ComponentState.STOPPED
        return True
        
    async def health_check(self) -> bool:
        return self.state == ComponentState.RUNNING
        
    def update_metric(self, name: str, value: Any):
        """Actualizar métrica"""
        self.monitored_metrics[name] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }

class ComponentRegistry:
    """Registro y gestor de componentes del sistema"""
    
    def __init__(self):
        self.components: Dict[str, BaseComponent] = {}
        self.component_classes: Dict[str, Type[BaseComponent]] = {}
        
    def load_components(self):
        """Cargar componentes por defecto"""
        self.register_component_class("logging", LoggingComponent)
        self.register_component_class("alerting", AlertingComponent)
        self.register_component_class("monitoring", MonitoringComponent)
        
        # Crear instancias por defecto
        self.create_component("logging", "logging")
        self.create_component("alerting", "alerting")
        self.create_component("monitoring", "monitoring")
        
    def register_component_class(self, name: str, component_class: Type[BaseComponent]):
        """Registrar una clase de componente"""
        if not issubclass(component_class, BaseComponent):
            raise ValueError("La clase debe heredar de BaseComponent")
        self.component_classes[name] = component_class
        
    def create_component(self, component_type: str, instance_name: str) -> bool:
        """Crear una nueva instancia de componente"""
        if component_type not in self.component_classes:
            return False
            
        try:
            component_class = self.component_classes[component_type]
            component = component_class()
            component.name = instance_name
            self.components[instance_name] = component
            return True
        except Exception as e:
            print(f"Error creando componente {instance_name}: {str(e)}")
            return False
            
    def replace_component(self, instance_name: str, new_component_type: str) -> bool:
        """Reemplazar un componente existente"""
        if instance_name not in self.components:
            return False
            
        old_component = self.components[instance_name]
        
        # Detener componente anterior
        if old_component.state == ComponentState.RUNNING:
            import asyncio
            asyncio.create_task(old_component.stop())
            
        # Crear nuevo componente
        if self.create_component(new_component_type, instance_name):
            return True
        else:
            # Si falla, mantener el componente anterior
            return False
            
    async def start_component(self, instance_name: str) -> bool:
        """Iniciar un componente"""
        if instance_name not in self.components:
            return False
        return await self.components[instance_name].start()
        
    async def stop_component(self, instance_name: str) -> bool:
        """Detener un componente"""
        if instance_name not in self.components:
            return False
        return await self.components[instance_name].stop()
        
    async def restart_component(self, instance_name: str) -> bool:
        """Reiniciar un componente"""
        if instance_name not in self.components:
            return False
            
        component = self.components[instance_name]
        if component.state == ComponentState.RUNNING:
            await component.stop()
        return await component.start()
        
    def remove_component(self, instance_name: str) -> bool:
        """Remover un componente"""
        if instance_name not in self.components:
            return False
            
        component = self.components[instance_name]
        if component.state == ComponentState.RUNNING:
            import asyncio
            asyncio.create_task(component.stop())
            
        del self.components[instance_name]
        return True
        
    def get_component(self, instance_name: str) -> Optional[BaseComponent]:
        """Obtener instancia de componente"""
        return self.components.get(instance_name)
        
    def list_components(self) -> Dict[str, Dict[str, Any]]:
        """Listar todos los componentes"""
        return {
            name: component.get_info()
            for name, component in self.components.items()
        }
        
    def list_component_types(self) -> List[str]:
        """Listar tipos de componentes disponibles"""
        return list(self.component_classes.keys())
        
    async def health_check_all(self) -> Dict[str, bool]:
        """Verificar salud de todos los componentes"""
        results = {}
        for name, component in self.components.items():
            try:
                results[name] = await component.health_check()
            except Exception as e:
                results[name] = False
        return results
        
    def get_component_count(self) -> int:
        """Obtener cantidad de componentes"""
        return len(self.components)