import time
from lib.sensor_dht22 import medir_temperatura, medir_humedad
from lib.oled_display import mostrar_datos
#print("importando lib,rtc...")
from lib.rtc import leer_fecha_hora

#import machine, os, vfs
# Slot 2 uses pins sck=18, cs=5, miso=19, mosi=23
import os, machine
from machine import SDCard, Pin
os.mount(machine.SDCard(slot=2, width=1, sck=18, cs=5, miso=19, mosi=23), "/sd")

# Listar archivos
# os.listdir()
# os mkdir("Lib")  # crear directorio Lib
# os.chdir("Lib")  # entrar a directorio Lib
# os.chdir("/")    # Salir y volver a directorio raiz
# os.rmdir("Lib")  # borrar directorio Lib
# os.getcwd()      # devuelve directorio actual (ubicación)
# os.rename("Lib","Libreria")   # Renombra el directorio
# ESCRIBIR ARCHIVO -----------------------
# file = open (file_name","mode")
#       mode   w   escribir (borra lo previo)
#              r   leer
#              a   agregar (append)
# file.write ("texto")
# file.write ('{},'.format(data))
# file.close()

os.listdir()
os.chdir("sd")
os.listdir()


#print("comenzando while true...")
while True:
    temp = medir_temperatura()
    time.sleep(0.5) # Evita errores en la toma de mediciones
    hum = medir_humedad()
    #print("medicion temp hum ok...")

    # Agregado de RTC
    now = leer_fecha_hora()
    year, month, date, day, hour, minute, second = now
    #print("lectura fecha hora ok...")
    
    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} Temperatura: {}°C Humedad: {}%'.format(year, month, date, hour, minute, second, temp, hum))
    
    file=open("Datalogger.txt","a")
    file.write ('{:02d},{:02d},{:02d},{:02d},{:02d},{:02d},{},{}\n'.format(year, month, date, hour, minute, second, temp, hum))
    file.close()
    
    mostrar_datos(temp, hum)

# Esperar 2 segundos antes de la siguiente lectura
    time.sleep(2)        