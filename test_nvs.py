DEBUG = True

WDTimer = True
NVStorage = True


import time
from machine import Pin
if WDTimer:
    from machine import WDT
    if DEBUG:
        print("importando lib.wdt...")
    wdt = WDT(timeout=5000)
if NVStorage:
    from machine import NVS
    if DEBUG:
        print("importando lib.nvs...")



if NVStorage:
    RESET_CODES={0:'PWRON',
                 1:'HARD',
                 2:'DEEPSLEEP',
                 3:'WDT',
                 4:'SOFT',
                 5:'BROWNOUT'}
    nvs = NVS('storage')
    reset_cause = machine.reset_cause()
    if DEBUG:
        print("reset cause: ",RESET_CODES[reset_cause])
    if reset_cause == 1:
        nvs.set('reset_count', nvs.get('reset_count', 0)+1)
    if DEBUG:
        print("almacenando en NVS...")

    # Imprimir el motivo del reinicio
    if DEBUG:
        print("reset count: ",nvs.get('reset_count'))




# Configuración del pin para el LED
led = Pin(2, Pin.OUT)

def parpadear_led():
    led.value(not led.value())

i = 1

while True:
    
    if WDTimer:
        wdt.feed()
        if DEBUG:
            print("reiniciar watchdog timer...")

    # Ejecutar las tareas
    parpadear_led()



    # Esperar 4 segundos antes de la siguiente lectura
    time.sleep(i)
    i=i+1