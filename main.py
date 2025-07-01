DEBUG = False
WIFI = False
RTC = True
OLED = True
DHT22 = True
MULTISENSOR = True
SD = False
WDTimer = True
NVStorage = False
reset_reason_str = 'None'
#==================Import=========================
import time
if WIFI:
    from lib.net import conectar_wifi  
    from lib.net import obtener_hora_actual
    if DEBUG:
        print("importando lib.net...")
if RTC:
    from lib.rtc import leer_fecha_hora
    if DEBUG:   
        print("importando lib,rtc...")
if OLED:
    from lib.oled_display import mostrar_datos
    if DEBUG:
        print("importando lib.oled_display...")
if DHT22:
    from lib.sensor_dht22 import medir_temperatura, medir_humedad
    if DEBUG:
        print("importando lib.sensor_dht22...")
if MULTISENSOR:
    from lib.multisensor import read_multisensor, read_multisensor_param
    import json
    import struct
    if DEBUG:
        print("importando lib.multisensor...")
if SD:
    import os, machine
    from machine import SDCard, Pin
    if DEBUG:
        print("importando lib.sd...")
    os.mount(machine.SDCard(slot=2, width=1, sck=18, cs=5, miso=19, mosi=23), "/sd")
    if DEBUG:
        print("montando SD Card...")
if WDTimer:
    from machine import WDT, reset_cause, DEEPSLEEP_RESET, HARD_RESET, SOFT_RESET, WDT_RESET, PWRON_RESET
    if DEBUG:
        print("importando lib.wdt...")
    wdt = WDT(timeout=10000)
if NVStorage:
    from machine import NVS
    if DEBUG:
        print("importando lib.nvs...")
    

#==================Inicializacion=========================

#==================Conexion WiFi=========================
if WIFI:
    conectar_wifi
    if DEBUG:
        print("conectando a wifi...")   
#==================Preparacion SD Card====================
if SD:
    os.listdir()
    os.chdir("sd")
    os.listdir()
    if DEBUG:
        print("preparando SD Card...")

if WDTimer:
    RESET_CODES = {
                    PWRON_RESET: 'PWRON',
                    HARD_RESET: 'HARD',
                    WDT_RESET: 'WDT',
                    DEEPSLEEP_RESET: 'DEEPSLEEP',
                    SOFT_RESET: 'SOFT',
                    }
    
    # Obtener el motivo del reinicio
    reset_reason = reset_cause()
    reset_reason_str = RESET_CODES.get(reset_reason, 'UNKNOWN')
    # Mostrar el motivo del reinicio por consola
    if DEBUG:
        print("Motivo del reinicio: ", reset_reason_str)
    
if NVStorage:        
    nvs = NVS('storage')
    if reset_cause == 1:
        nvs.set('reset_count', nvs.get('reset_count', 0)+1)
    if DEBUG:
        print("almacenando en NVS...")


while True:
    
    if WDTimer:
        wdt.feed()
        if DEBUG:
            print("reiniciar watchdog timer...")

    if WIFI:
        datos_hora = obtener_hora_actual()
        
    if DHT22:
        temp = medir_temperatura()
        time.sleep(0.5) # Evita errores en la toma de mediciones
        hum = medir_humedad()
        if DEBUG:       
            print("medicion temp hum ok...")
        time.sleep(1)
        if DEBUG:
            if temp is not None:
               print('Temperatura: {}°C'.format(temp))
            if hum is not None:
               print('Humedad: {}%'.format(hum))
    
    if RTC: 
        now = leer_fecha_hora()
        year, month, date, day, hour, minute, second = now
        if DEBUG:
            print("lectura fecha hora ok...")   
            if now is not None:
               print('Hora: {}'.format(now))

    if MULTISENSOR:
        #value = read_multisensor_param()
        (co2,voc,humidity,temp_ms,pm25) = read_multisensor()

        if DEBUG:
            print("lectura multisensor ok...")
            #print (json.dumps(value))        


    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} Temp_DHT: {}°C Humedad_DHT: {}% Temp_Ms: {}°C Humidity_Ms: {}% PM2.5: {} reset_reason {}'.format(year, month, date, hour, minute, second, temp, hum, temp_ms, humidity, pm25, reset_reason_str))
    if OLED:
        mostrar_datos(temp, hum)

    if SD:
        file=open("Datalogger.txt","a")
        file.write ('{:02d},{:02d},{:02d},{:02d},{:02d},{:02d},{},{},{},{},{}\n'.format(year, month, date, hour, minute, second, temp, hum, temp_ms, humidity, pm25))
        file.close()
        if DEBUG:
            print("escribiendo en SD Card...")
            
    if WDTimer:
        if reset_reason_str != 'None':
            reset_reason_str = 'None'

    # Esperar 2 segundos antes de la siguiente lectura
    time.sleep(4)        