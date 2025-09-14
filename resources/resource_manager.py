"""
Sistema de gestión de recursos externos
Los recursos se almacenan en archivos externos para facilitar 
su modificación sin necesidad de volver a compilar y desplegar
"""

import json
import yaml
import os
from typing import Dict, Any, Optional
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class ResourceChangeHandler(FileSystemEventHandler):
    """Manejador para detectar cambios en archivos de recursos"""
    
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if filename in self.resource_manager.watched_files:
                print(f"Archivo de recurso modificado: {filename}")
                self.resource_manager.reload_resource(event.src_path)

class ResourceManager:
    """Gestor de recursos externos"""
    
    def __init__(self, resource_dir: str = "config/resources"):
        self.resource_dir = resource_dir
        self.resources: Dict[str, Any] = {}
        self.file_timestamps: Dict[str, float] = {}
        self.watched_files: set = set()
        self.observer = None
        self._lock = threading.Lock()
        
        # Crear directorio si no existe
        os.makedirs(resource_dir, exist_ok=True)
        
    def load_resources(self):
        """Cargar todos los recursos desde archivos"""
        self._create_default_resources()
        self._load_all_resource_files()
        self._setup_file_watcher()
        
    def _create_default_resources(self):
        """Crear archivos de recursos por defecto para la demo"""
        
        # Configuración de la aplicación
        app_config = {
            "app_name": "Sistema de Monitoreo",
            "version": "1.0.0",
            "debug": True,
            "max_alerts": 1000,
            "default_check_interval": 10,
            "alert_retention_days": 30
        }
        
        # Umbrales de monitoreo
        monitoring_thresholds = {
            "cpu_max_percentage": 80,
            "memory_min_mb": 100,
            "temperature_min": 20,
            "temperature_max": 80,
            "disk_min_free_gb": 1
        }
        
        # Mensajes de alerta
        alert_messages = {
            "cpu_high": "Uso de CPU elevado detectado",
            "memory_low": "Memoria disponible baja",
            "temperature_out_of_range": "Temperatura fuera del rango normal",
            "disk_space_low": "Espacio en disco bajo",
            "network_down": "Conectividad de red perdida"
        }
        
        # Configuración de componentes
        component_config = {
            "enabled_components": ["monitoring", "alerting", "logging"],
            "component_timeout": 30,
            "auto_restart": True,
            "max_retries": 3
        }
        
        # Guardar archivos
        self._save_resource("app_config.json", app_config)
        self._save_resource("monitoring_thresholds.yaml", monitoring_thresholds)
        self._save_resource("alert_messages.json", alert_messages)
        self._save_resource("component_config.yaml", component_config)
        
    def _save_resource(self, filename: str, data: Dict[str, Any]):
        """Guardar un recurso en archivo"""
        filepath = os.path.join(self.resource_dir, filename)
        
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                
    def _load_all_resource_files(self):
        """Cargar todos los archivos de recursos"""
        if not os.path.exists(self.resource_dir):
            return
            
        for filename in os.listdir(self.resource_dir):
            filepath = os.path.join(self.resource_dir, filename)
            if os.path.isfile(filepath):
                self.reload_resource(filepath)
                
    def reload_resource(self, filepath: str):
        """Recargar un recurso específico"""
        try:
            with self._lock:
                filename = os.path.basename(filepath)
                
                # Verificar si el archivo cambió
                current_mtime = os.path.getmtime(filepath)
                if (filename in self.file_timestamps and 
                    self.file_timestamps[filename] >= current_mtime):
                    return
                
                # Cargar contenido según extensión
                if filename.endswith('.json'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                elif filename.endswith('.yaml') or filename.endswith('.yml'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                else:
                    # Archivo de texto plano
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = f.read()
                
                # Almacenar recurso
                resource_name = os.path.splitext(filename)[0]
                self.resources[resource_name] = data
                self.file_timestamps[filename] = current_mtime
                self.watched_files.add(filename)
                
                print(f"Recurso '{resource_name}' cargado desde {filename}")
                
        except Exception as e:
            print(f"Error cargando recurso {filepath}: {str(e)}")
            
    def _setup_file_watcher(self):
        """Configurar observador de cambios en archivos"""
        if self.observer:
            self.observer.stop()
            
        self.observer = Observer()
        handler = ResourceChangeHandler(self)
        self.observer.schedule(handler, self.resource_dir, recursive=False)
        self.observer.start()
        
    def get_resource(self, name: str, default: Any = None) -> Any:
        """Obtener un recurso por nombre"""
        return self.resources.get(name, default)
        
    def set_resource(self, name: str, value: Any, save_to_file: bool = False):
        """Establecer un recurso en memoria y opcionalmente guardarlo"""
        with self._lock:
            self.resources[name] = value
            
            if save_to_file:
                filename = f"{name}.json"
                self._save_resource(filename, value)
                
    def get_all_resources(self) -> Dict[str, Any]:
        """Obtener todos los recursos"""
        return self.resources.copy()
        
    def get_resource_info(self) -> Dict[str, Any]:
        """Obtener información sobre los recursos cargados"""
        return {
            "total_resources": len(self.resources),
            "resource_directory": self.resource_dir,
            "watched_files": list(self.watched_files),
            "last_loaded": {
                name: datetime.fromtimestamp(timestamp).isoformat()
                for name, timestamp in self.file_timestamps.items()
            }
        }
        
    def reload_all_resources(self):
        """Recargar todos los recursos"""
        self.resources.clear()
        self.file_timestamps.clear()
        self._load_all_resource_files()
        
    def get_resource_count(self) -> int:
        """Obtener cantidad de recursos cargados"""
        return len(self.resources)
        
    def stop_watcher(self):
        """Detener el observador de archivos"""
        if self.observer:
            self.observer.stop()
            self.observer.join()