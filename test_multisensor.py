import machine
import time
import json
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
    
def convert(s):
    if s != None:
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B:
          return {'co2': s[3]*256 + s[4],
                  'voc': s[5]*256 + s[6],
                  'humidity': (s[7]*256 + s[8])*0.1,
                  'temperature': ((s[9]*256 + s[10])-500)*0.1,
                  'pm2.5': s[11]*256 + s[12]
                  }
           
def read_all():
    write_data(b"\x11\x02\x01\x00\xEC")
    s=read_data()
    if s != None:    
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B:
          return {'co2': s[3]*256 + s[4],
                  'voc': s[5]*256 + s[6],
                  'humidity': (s[7]*256 + s[8])*0.1,
                  'temperature': ((s[9]*256 + s[10])-500)*0.1,
                  'pm2.5': s[11]*256 + s[12]
                  }

    
while True:

    value = read_all()
    print (json.dumps(value))

    #write_data(b"\x11\x02\x01\x00\xEC")
    #s=read_data()
    #print("Received:", s)
    #print (json.dumps(convert(s)))
    #abc_off()
    time.sleep(10)    