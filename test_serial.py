import machine
import time
import struct
import os

# Determine the UART port to use
uart_port = 2
# Initialize UART
uart = machine.UART(uart_port, baudrate=9600, tx=17, rx=16)  # Adjust TX and RX pins as needed

def read_data():
    if uart.any() > 0:
        data = uart.read()
        return data
    return None

def write_data(data):
    uart.write(data)
    
while True:
    rxData = read_data()

    if rxData != None:
        print(rxData)
        if 'on' in rxData:
            print('ON')
            print("Received:", rxData)
    time.sleep(1)    