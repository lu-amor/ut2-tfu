#!/usr/bin/env python3
"""
Script de demostración para mostrar las características del sistema:
- Monitoreo de condiciones 
- Archivos de recursos externos
- Reemplazo de componentes
"""

import requests
import time
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
DELAY = 2  # segundos entre operaciones

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n--- {title} ---")

def make_request(method, endpoint, **kwargs):
    """Hacer petición HTTP con manejo de errores"""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        if response.status_code >= 400:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
        return response.json()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose?")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def demo_monitoring():
    """Demostrar funcionalidades de monitoreo"""
    print_header("DEMOSTRACIÓN: MONITOREO DE CONDICIONES")
    
    print_section("1. Estado del sistema de monitoreo")
    status = make_request("GET", "/api/monitoring/status")
    if status:
        print(f"✅ Sistema ejecutándose: {status['is_running']}")
        print(f"📊 Condiciones totales: {status['total_conditions']}")
        print(f"🔍 Condiciones habilitadas: {status['enabled_conditions']}")
        print(f"🚨 Alertas totales: {status['total_alerts']}")
    
    time.sleep(DELAY)
    
    print_section("2. Condiciones monitoreadas")
    conditions = make_request("GET", "/api/monitoring/conditions")
    if conditions:
        for condition in conditions:
            icon = "✅" if condition['enabled'] else "⏸️"
            print(f"{icon} {condition['name']}: {condition['description']}")
            print(f"   Nivel: {condition['alert_level']}, Intervalo: {condition['check_interval']}s")
    
    time.sleep(DELAY)
    
    print_section("3. Alertas existentes")
    alerts = make_request("GET", "/api/monitoring/alerts?limit=5")
    if alerts:
        if len(alerts) > 0:
            for alert in alerts:
                level_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "critical": "🔥"}.get(alert['level'], "❓")
                print(f"{level_icon} [{alert['level'].upper()}] {alert['message']}")
                print(f"   Condición: {alert['condition_name']}, Valor: {alert['current_value']}")
        else:
            print("ℹ️ No hay alertas registradas")
    
    time.sleep(DELAY)
    
    print_section("4. Crear alerta de prueba")
    test_alert = make_request("POST", "/api/monitoring/test-alert")
    if test_alert:
        print(f"✅ {test_alert['message']}")
        print(f"🆔 ID de alerta: {test_alert['alert_id']}")
    
    time.sleep(DELAY)
    
    print_section("5. Deshabilitar una condición")
    disable_result = make_request("POST", "/api/monitoring/conditions/temperature_sensor/enable?enabled=false")
    if disable_result:
        print(f"✅ {disable_result['message']}")

def demo_resources():
    """Demostrar gestión de recursos externos"""
    print_header("DEMOSTRACIÓN: ARCHIVOS DE RECURSOS EXTERNOS")
    
    print_section("1. Recursos cargados desde archivos")
    resources = make_request("GET", "/api/resources/")
    if resources:
        for resource in resources:
            print(f"📄 {resource['name']} ({resource['type']})")
            if isinstance(resource['value'], dict) and len(resource['value']) <= 5:
                for key, value in resource['value'].items():
                    print(f"   {key}: {value}")
            else:
                print(f"   Contenido: {str(resource['value'])[:100]}...")
    
    time.sleep(DELAY)
    
    print_section("2. Información del sistema de recursos")
    summary = make_request("GET", "/api/resources/info/summary")
    if summary:
        print(f"📊 Total de recursos: {summary['total_resources']}")
        print(f"📁 Directorio: {summary['resource_directory']}")
        print(f"👀 Archivos monitoreados: {len(summary['watched_files'])}")
        for file in summary['watched_files']:
            print(f"   - {file}")
    
    time.sleep(DELAY)
    
    print_section("3. Archivos de recursos disponibles")
    files = make_request("GET", "/api/resources/files/list")
    if files:
        print(f"📁 Directorio: {files['directory']}")
        print(f"📄 Total de archivos: {files['total_files']}")
        for file in files['files']:
            print(f"   - {file['name']} ({file['size']} bytes, {file['extension']})")
    
    time.sleep(DELAY)
    
    print_section("4. Obtener recurso específico")
    app_config = make_request("GET", "/api/resources/app_config")
    if app_config:
        print(f"📋 Configuración de la aplicación:")
        config = app_config['value']
        for key, value in config.items():
            print(f"   {key}: {value}")
    
    time.sleep(DELAY)
    
    print_section("5. Recargar todos los recursos")
    reload_result = make_request("POST", "/api/resources/reload")
    if reload_result:
        print(f"✅ {reload_result['message']}")
        print(f"📊 Recursos cargados: {reload_result['resources_loaded']}")

def demo_components():
    """Demostrar reemplazo de componentes"""
    print_header("DEMOSTRACIÓN: REEMPLAZO DE COMPONENTES")
    
    print_section("1. Componentes disponibles")
    components = make_request("GET", "/api/components/")
    if components:
        for component in components:
            state_icon = {"stopped": "⏹️", "running": "▶️", "error": "❌"}.get(component['state'], "❓")
            print(f"{state_icon} {component['name']} ({component['class_name']})")
            print(f"   Estado: {component['state']}")
            if component['start_time']:
                print(f"   Iniciado: {component['start_time']}")
    
    time.sleep(DELAY)
    
    print_section("2. Tipos de componentes disponibles")
    types = make_request("GET", "/api/components/types")
    if types:
        print(f"🔧 Tipos disponibles: {types['total_types']}")
        for comp_type in types['available_types']:
            print(f"   - {comp_type}")
    
    time.sleep(DELAY)
    
    print_section("3. Iniciar componente de logging")
    start_result = make_request("POST", "/api/components/logging/start")
    if start_result:
        print(f"✅ {start_result['message']}")
    
    time.sleep(DELAY)
    
    print_section("4. Verificar salud de componentes")
    health = make_request("GET", "/api/components/health/all")
    if health:
        for component_health in health:
            health_icon = "✅" if component_health['healthy'] else "❌"
            print(f"{health_icon} {component_health['component_name']}: {'Saludable' if component_health['healthy'] else 'Con problemas'}")
    
    time.sleep(DELAY)
    
    print_section("5. Crear nuevo componente")
    create_result = make_request("POST", "/api/components/create?component_type=alerting&instance_name=alerting_backup")
    if create_result:
        print(f"✅ {create_result['message']}")
    
    time.sleep(DELAY)
    
    print_section("6. Reemplazar componente")
    replace_result = make_request("PUT", "/api/components/alerting_backup/replace?new_component_type=monitoring")
    if replace_result:
        print(f"✅ {replace_result['message']}")
    
    time.sleep(DELAY)
    
    print_section("7. Estado final de componentes")
    final_components = make_request("GET", "/api/components/")
    if final_components:
        for component in final_components:
            state_icon = {"stopped": "⏹️", "running": "▶️", "error": "❌"}.get(component['state'], "❓")
            print(f"{state_icon} {component['name']} ({component['class_name']}) - {component['state']}")

def main():
    """Función principal de la demostración"""
    print_header("DEMO: SISTEMA DE MONITOREO Y GESTIÓN DE COMPONENTES")
    print("Este script demuestra las tres características principales:")
    print("1. 🔍 Monitoreo de condiciones con alertas")
    print("2. 📄 Gestión de recursos externos")
    print("3. 🔄 Reemplazo dinámico de componentes")
    print(f"\nConectando a: {BASE_URL}")
    
    # Verificar que el servidor esté ejecutándose
    health = make_request("GET", "/health")
    if not health:
        print("\n❌ No se puede conectar al servidor.")
        print("Por favor, ejecute: python main.py")
        return
    
    print(f"\n✅ Servidor conectado - Estado: {health['status']}")
    
    # Ejecutar demos
    demo_monitoring()
    demo_resources()
    demo_components()
    
    print_header("DEMOSTRACIÓN COMPLETADA")
    print("✅ Se han demostrado todas las características del sistema:")
    print("   🔍 Monitoreo automático de condiciones")
    print("   📄 Carga dinámica de recursos desde archivos")
    print("   🔄 Reemplazo en tiempo real de componentes")
    print("\nPara más información, visite: http://localhost:8000/docs")

if __name__ == "__main__":
    main()