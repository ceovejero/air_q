# Sistema de Monitoreo de Calidad del Aire con ESP32

## Descripción

Sistema integral de monitoreo ambiental utilizando ESP32 que recopila datos de múltiples sensores para medir temperatura, humedad, calidad del aire (CO2, VOC, PM2.5) y registra la información tanto en pantalla OLED como en archivos de datos.

## Características Principales

- **Monitoreo Multi-sensor**: DHT22 + Multisensor de calidad del aire
- **Visualización**: Pantalla OLED SSD1306 128x64
- **Almacenamiento**: Tarjeta SD con logging CSV
- **Conectividad**: WiFi opcional para sincronización de tiempo
- **Reloj en tiempo real**: DS1307 RTC
- **Watchdog Timer**: Protección contra cuelgues del sistema
- **Arquitectura modular**: Código organizado y mantenible

## Hardware Requerido

### Componentes Principales
- **ESP32 Dev Kit V1** - Microcontrolador principal
- **DHT22** - Sensor de temperatura y humedad
- **Multisensor de calidad del aire** - CO2, VOC, PM2.5
- **Pantalla OLED SSD1306** (128x64, I2C)
- **Módulo RTC DS1307** - Reloj en tiempo real
- **Módulo SD Card** - Almacenamiento de datos
- **Resistencias pull-up** 4.7kΩ para I2C

### Diagrama de Conexiones

```
ESP32 Pin    |  Dispositivo        |  Pin/Cable
-------------|---------------------|-------------
GPIO 14      |  DHT22              |  Data
GPIO 22      |  OLED & RTC         |  SCL (I2C)
GPIO 21      |  OLED & RTC         |  SDA (I2C)
GPIO 17      |  Multisensor        |  TX (UART)
GPIO 16      |  Multisensor        |  RX (UART)
GPIO 18      |  SD Card            |  SCK
GPIO 5       |  SD Card            |  CS
GPIO 19      |  SD Card            |  MISO
GPIO 23      |  SD Card            |  MOSI
3.3V         |  Todos              |  VCC
GND          |  Todos              |  GND
```

## Estructura del Proyecto

```
air_q/
├── main.py                 # Archivo principal del sistema
├── config.py              # Configuración centralizada
├── boot.py                # Configuración de arranque
├── lib/                   # Librerías del sistema
│   ├── logger.py          # Sistema de logging
│   ├── data_manager.py    # Gestor de datos centralizado
│   ├── sensor_dht22.py    # Driver mejorado DHT22
│   ├── multisensor.py     # Driver multisensor mejorado
│   ├── oled_display.py    # Control de pantalla OLED
│   ├── rtc.py            # Manejo del RTC DS1307
│   ├── net.py            # Conectividad WiFi
│   └── ssd1306.py        # Driver OLED (MicroPython)
├── test_*.py             # Scripts de prueba individuales
└── README.MD             # Esta documentación
```

## Instalación y Configuración

### 1. Preparar el ESP32

```bash
# Instalar MicroPython en ESP32
# Descargar firmware desde: https://micropython.org/download/esp32/
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 write_flash -z 0x1000 esp32-20240222-v1.22.2.bin
```

### 2. Configurar el Proyecto

1. **Editar `config.py`** para personalizar:
   - Pines GPIO según tu circuito
   - Credenciales WiFi
   - Intervalos de medición
   - Características a habilitar/deshabilitar

2. **Subir archivos al ESP32**:
   ```bash
   # Usando ampy
   ampy -p /dev/ttyUSB0 put main.py
   ampy -p /dev/ttyUSB0 put config.py
   ampy -p /dev/ttyUSB0 put -r lib/
   
   # O usando Thonny IDE
   # Abrir Thonny → Herramientas → Opciones → Intérprete → MicroPython (ESP32)
   ```

### 3. Configuración Inicial

```python
# En config.py - Habilitar/deshabilitar características
DEBUG = True        # Para depuración inicial
WIFI = True         # Si tienes conectividad WiFi
RTC = True          # Si instalaste el módulo RTC
OLED = True         # Si instalaste la pantalla
DHT22 = True        # Sensor principal
MULTISENSOR = True  # Sensor de calidad del aire
SD = True           # Si instalaste módulo SD
WDT_TIMER = True    # Recomendado mantener activo
NV_STORAGE = False  # Opcional
```

## Uso del Sistema

### Inicio Automático
El sistema inicia automáticamente al encender el ESP32. El archivo `main.py` ejecuta el bucle principal.

### Monitoreo en Tiempo Real
```
Data Log: 24:01:05:14:30:25 Temp_DHT: 23.5°C Humedad_DHT: 60% 
Temp_Ms: 23.2°C Humidity_Ms: 58% PM2.5: 15 CO2: 420 VOC: 0.1 reset_reason PWRON
```

### Datos Almacenados (CSV)
```csv
24,01,05,14,30,25,23.5,60,23.2,58,15,420,0.1
año,mes,día,hora,min,seg,temp_dht,hum_dht,temp_ms,hum_ms,pm25,co2,voc
```

## Scripts de Prueba

Cada componente incluye scripts de prueba individuales:

- `test_dht22.py` - Prueba sensor DHT22
- `test_oled.py` - Prueba pantalla OLED
- `test_rtc.py` - Prueba módulo RTC
- `test_multisensor.py` - Prueba sensor de calidad del aire
- `test_sd.py` - Prueba módulo SD Card
- `test_nvs.py` - Prueba almacenamiento no volátil

## API del Sistema

### Clases Principales

#### `DataManager`
```python
# Gestor centralizado de datos
data_manager = DataManager()
data_manager.update_dht22_data(temp, humidity)
data_manager.save_to_file()
log_string = data_manager.get_formatted_log_string()
```

#### `DHT22Sensor`
```python
# Sensor DHT22 mejorado
dht = DHT22Sensor(pin=14)
temp, hum = dht.get_readings()
```

#### `MultiSensor`
```python
# Sensor de calidad del aire
ms = MultiSensor()
data = ms.read_all_parameters()  # Retorna dict
co2, voc, hum, temp, pm25 = ms.read_sensor_tuple()  # Retorna tupla
```

#### `Logger`
```python
# Sistema de logging
from lib.logger import Logger
Logger.info("Sistema iniciado")
Logger.error("Error en sensor")
Logger.debug("Valor de debug")
```

## Configuración Avanzada

### Calibración de Sensores
```python
# En config.py - Ajustes de calibración
class CalibrationConfig:
    DHT22_TEMP_OFFSET = 0.0      # Offset temperatura DHT22
    DHT22_HUM_OFFSET = 0.0       # Offset humedad DHT22
    MS_TEMP_OFFSET = 0.0         # Offset temperatura multisensor
    CO2_CALIBRATION = 400        # Valor base CO2 en aire limpio
```

### Intervalos de Medición
```python
# En config.py - TimerConfig
SENSOR_READ_INTERVAL = 4         # Intervalo principal (segundos)
DHT22_MIN_INTERVAL = 2000        # Mínimo entre lecturas DHT22 (ms)
MULTISENSOR_INTERVAL = 1000      # Mínimo multisensor (ms)
WDT_TIMEOUT = 10000             # Timeout watchdog (ms)
```

## Solución de Problemas

### Problemas Comunes

1. **Error "OSError: [Errno 19] ENODEV"**
   - Verificar conexiones I2C (SDA/SCL)
   - Comprobar alimentación de 3.3V
   - Verificar resistencias pull-up

2. **Sensor DHT22 retorna None**
   - Verificar pin de datos conectado
   - Esperar 2 segundos entre lecturas
   - Verificar alimentación estable

3. **Multisensor no responde**
   - Verificar conexiones UART (TX/RX)
   - Comprobar baudrate (9600)
   - Verificar protocolo de comunicación

4. **SD Card no monta**
   - Verificar formato FAT32
   - Comprobar conexiones SPI
   - Verificar alimentación 3.3V

### Modo Debug
```python
# Activar en config.py
DEBUG = True

# Ver logs detallados
[INFO 12345] DHT22 inicializado en pin 14
[DEBUG 12350] DHT22 - Temp: 23.5°C, Hum: 60%
[ERROR 12355] Error en sensor DHT22: OSError
```

## Contribuir al Proyecto

1. Fork el repositorio
2. Crear rama para nueva característica
3. Implementar mejoras siguiendo el estilo del código
4. Agregar tests apropiados
5. Documentar cambios en README
6. Crear Pull Request

## Roadmap

### Versión 2.1 (Próxima)
- [ ] Calibración automática de sensores
- [ ] Interfaz web para configuración
- [ ] Alertas por thresholds configurables
- [ ] Soporte para múltiples tipos de multisensor

### Versión 2.2 (Futuro)
- [ ] Integración con servicios en la nube
- [ ] Dashboard de visualización de datos
- [ ] Predicción de calidad del aire
- [ ] Soporte para sensores adicionales

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para detalles.

## Soporte y Contacto

- **Issues**: Reportar bugs en GitHub Issues
- **Documentación**: Wiki del proyecto
- **Simulación**: [Wokwi](https://wokwi.com/projects/416204083798477825)
- **Datos en vivo**: [Google Sheets](https://docs.google.com/spreadsheets/d/1pcTxw9gxgdikChK3UODAOqdXHpwWqttbv10XZhzlk24/edit)

---

**Estado del Proyecto**: Activo ✅  
**Última actualización**: Enero 2025  
**Versión**: 2.0

2. **Obtener la hora actual**:
   La función `obtener_hora_actual` obtiene la hora actual desde la API de World Time.

3. **Leer datos del sensor DHT22**:
   Las funciones `medir_temperatura` y `medir_humedad` leen los datos de temperatura y humedad del sensor DHT22.

4. **Mostrar datos en la pantalla OLED**:
   La función `mostrar_datos` muestra los datos en la pantalla OLED SSD1306.

5. **Enviar datos a Google Sheets y Excel Online**:
   Las funciones `cargar_datos` en `google_sheets.py` y `microsoft_excel.py` envían los datos a las respectivas hojas de cálculo.

## Funcionalidad en Desarrollo

### Enviar los datos de las mediciones a una hoja de cálculos de Google

**[Ver Hoja de Calculo](https://docs.google.com/spreadsheets/d/1pcTxw9gxgdikChK3UODAOqdXHpwWqttbv10XZhzlk24/edit?gid=0#gid=0)**

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.



