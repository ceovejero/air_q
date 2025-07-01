import time
from machine import Pin, WDT, reset_cause, DEEPSLEEP_RESET, HARD_RESET, SOFT_RESET, WDT_RESET, PWRON_RESET
#from machine import NVS

# Configuración de depuración
DEBUG = True

# Inicializar el Watchdog Timer con un tiempo de espera de 5 segundos
wdt = WDT(timeout=5000)

# Inicializar NVS
#nvs = NVS('storage')

# Diccionario de códigos de reinicio
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

# Incrementar el contador de reinicios en NVS
#reset_count = nvs.get('reset_count', 0) + 1
#nvs.set('reset_count', reset_count)

# Mostrar el contador de reinicios por consola
#if DEBUG:
#    print("Contador de reinicios: ", reset_count)

# Configuración del pin para el LED
led = Pin(2, Pin.OUT)

def parpadear_led():
    led.value(not led.value())

i = 1

# Bucle principal
while True:
    # Reiniciar el Watchdog Timer
    wdt.feed()
    if DEBUG:
        print("Reiniciar Watchdog Timer...")

    # Ejecutar la función de parpadeo del LED
    parpadear_led()

    # Esperar 1 segundo antes de la siguiente iteración
    time.sleep(i)
    i = i +1