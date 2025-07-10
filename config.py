# Configuración centralizada del proyecto
# =====================================

# Configuración de características
DEBUG = False
WIFI = False
RTC = True
OLED = True
DHT22 = True
MULTISENSOR = True
SD = False
WDT_TIMER = True
NV_STORAGE = False

# Configuración de pines GPIO
class PinConfig:
    # DHT22
    DHT22_PIN = 14
    
    # I2C (OLED y RTC)
    I2C_SCL = 22
    I2C_SDA = 21
    I2C_FREQ = 400000
    
    # UART (Multisensor)
    UART_TX = 17
    UART_RX = 16
    UART_BAUDRATE = 9600
    UART_PORT = 2
    
    # SD Card
    SD_SCK = 18
    SD_CS = 5
    SD_MISO = 19
    SD_MOSI = 23
    SD_SLOT = 2
    
    # LED
    LED_PIN = 2

# Configuración de red WiFi
class WiFiConfig:
    SSID = 'CEO_WiFi'
    PASSWORD = 'abc12345'
    TIME_API_URL = 'http://worldtimeapi.org/api/timezone/America/Argentina/Tucuman'

# Configuración de temporizadores
class TimerConfig:
    WDT_TIMEOUT = 10000  # ms
    SENSOR_READ_INTERVAL = 4  # segundos
    DHT22_DELAY = 0.5  # segundos entre lecturas
    MULTISENSOR_INTERVAL = 1  # segundos

# Configuración de archivos
class FileConfig:
    DATA_LOG_FILE = "Datalogger.txt"
    NVS_NAMESPACE = 'storage'

# Configuración OLED
class OLEDConfig:
    WIDTH = 128
    HEIGHT = 64
