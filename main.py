"""
Sistema de Monitoreo de Calidad del Aire
Versión 2.0 - Mejorada
"""
import time
from config import *
from lib.logger import Logger, ErrorHandler
from lib.data_manager import DataManager

# Importaciones condicionales mejoradas
def import_modules():
    """Importa los módulos según la configuración"""
    modules = {}
    
    try:
        if WIFI:
            from lib.net import conectar_wifi, obtener_hora_actual
            modules['wifi'] = {'conectar': conectar_wifi, 'hora': obtener_hora_actual}
            Logger.info("Módulo WiFi importado")
        
        if RTC:
            from lib.rtc import leer_fecha_hora
            modules['rtc'] = leer_fecha_hora
            Logger.info("Módulo RTC importado")
        
        if OLED:
            from lib.oled_display import mostrar_datos
            modules['oled'] = mostrar_datos
            Logger.info("Módulo OLED importado")
        
        if DHT22:
            from lib.sensor_dht22 import DHT22Sensor
            modules['dht22'] = DHT22Sensor()
            Logger.info("Sensor DHT22 inicializado")
        
        if MULTISENSOR:
            from lib.multisensor import MultiSensor
            modules['multisensor'] = MultiSensor()
            Logger.info("Multisensor inicializado")
        
        if SD:
            import os, machine
            from machine import SDCard, Pin
            os.mount(machine.SDCard(
                slot=PinConfig.SD_SLOT, width=1, 
                sck=PinConfig.SD_SCK, cs=PinConfig.SD_CS, 
                miso=PinConfig.SD_MISO, mosi=PinConfig.SD_MOSI
            ), "/sd")
            os.chdir("sd")
            Logger.info("SD Card montada")
        
        if WDT_TIMER:
            from machine import WDT, reset_cause
            from machine import DEEPSLEEP_RESET, HARD_RESET, SOFT_RESET, WDT_RESET, PWRON_RESET
            
            modules['wdt'] = WDT(timeout=TimerConfig.WDT_TIMEOUT)
            modules['reset_codes'] = {
                PWRON_RESET: 'PWRON',
                HARD_RESET: 'HARD',
                WDT_RESET: 'WDT',
                DEEPSLEEP_RESET: 'DEEPSLEEP',
                SOFT_RESET: 'SOFT',
            }
            modules['reset_reason'] = modules['reset_codes'].get(reset_cause(), 'UNKNOWN')
            Logger.info("Watchdog Timer inicializado")
        
        if NV_STORAGE:
            from machine import NVS
            modules['nvs'] = NVS(FileConfig.NVS_NAMESPACE)
            Logger.info("NV Storage inicializado")
            
    except Exception as e:
        ErrorHandler.handle_sensor_error("importación de módulos", e)
    
    return modules

def initialize_system():
    """Inicializa el sistema completo"""
    Logger.info("=== Iniciando Sistema de Monitoreo ===")
    
    # Importar módulos
    modules = import_modules()
    
    # Inicializar gestor de datos
    data_manager = DataManager()
    
    # Configurar WiFi si está habilitado
    if WIFI and 'wifi' in modules:
        try:
            modules['wifi']['conectar']()
            Logger.info("WiFi conectado exitosamente")
        except Exception as e:
            ErrorHandler.handle_network_error("conexión WiFi", e)
    
    # Configurar reset reason
    if WDT_TIMER and 'reset_reason' in modules:
        data_manager.update_reset_reason(modules['reset_reason'])
        Logger.info(f"Motivo del reinicio: {modules['reset_reason']}")
    
    return modules, data_manager

def read_sensors(modules, data_manager):
    """Lee todos los sensores disponibles"""
    
    # Leer RTC
    if RTC and 'rtc' in modules:
        try:
            year, month, date, day, hour, minute, second = modules['rtc']()
            data_manager.update_timestamp(year, month, date, hour, minute, second)
        except Exception as e:
            ErrorHandler.handle_sensor_error("RTC", e)
    
    # Leer DHT22
    if DHT22 and 'dht22' in modules:
        try:
            temp, hum = modules['dht22'].get_readings()
            if temp is not None and hum is not None:
                data_manager.update_dht22_data(temp, hum)
        except Exception as e:
            ErrorHandler.handle_sensor_error("DHT22", e)
    
    # Leer Multisensor
    if MULTISENSOR and 'multisensor' in modules:
        try:
            sensor_data = modules['multisensor'].read_all_parameters()
            if sensor_data:
                data_manager.update_multisensor_data(
                    sensor_data['co2'], sensor_data['voc'],
                    sensor_data['humidity'], sensor_data['temperature'],
                    sensor_data['pm2.5']
                )
        except Exception as e:
            ErrorHandler.handle_sensor_error("Multisensor", e)

def main_loop():
    """Bucle principal del sistema"""
    modules, data_manager = initialize_system()
    
    Logger.info("=== Iniciando bucle principal ===")
    
    while True:
        try:
            # Alimentar watchdog
            if WDT_TIMER and 'wdt' in modules:
                modules['wdt'].feed()
                Logger.debug("Watchdog alimentado")
            
            # Leer sensores
            read_sensors(modules, data_manager)
            
            # Mostrar datos
            print(data_manager.get_formatted_log_string())
            
            # Actualizar OLED
            if OLED and 'oled' in modules:
                temp, hum = data_manager.get_oled_data()
                if temp is not None and hum is not None:
                    modules['oled'](temp, hum)
            
            # Guardar en SD
            if SD:
                data_manager.save_to_file()
            
            # Obtener hora de internet si está habilitado
            if WIFI and 'wifi' in modules:
                try:
                    hora_internet = modules['wifi']['hora']()
                    if hora_internet:
                        Logger.debug(f"Hora de internet: {hora_internet}")
                except Exception as e:
                    ErrorHandler.handle_network_error("obtener hora", e)
            
            # Esperar antes de la siguiente lectura
            time.sleep(TimerConfig.SENSOR_READ_INTERVAL)
            
        except KeyboardInterrupt:
            Logger.info("Sistema detenido por el usuario")
            break
        except Exception as e:
            ErrorHandler.handle_sensor_error("bucle principal", e)
            time.sleep(1)  # Esperar antes de continuar

if __name__ == "__main__":
    main_loop()        