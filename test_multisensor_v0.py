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
    
def read_all():
    write_data(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    s=read_data()
    if s != None:
        if len(s) >= 9 and s[0] == "\xff" and s[1] == "\x86":
          return {'pm1.0': ord(s[2])*256 + ord(s[3]),
                  'pm2.5': ord(s[4])*256 + ord(s[5]),
                  'pm10': ord(s[6])*256 + ord(s[7]),
                  'co2': ord(s[8])*256 + ord(s[9]),
                  'voc': ord(s[10]),
                  'temperature': ((ord(s[11])*256 + ord(s[12]))-435)*0.1,
                  'rh': ord(s[13])*256 + ord(s[14]),
                  'ch2o': (ord(s[15])*256 + ord(s[16]))*0.001,
                  'co': (ord(s[17])*256 + ord(s[18]))*0.1,
                  'o3': (ord(s[19])*256 + ord(s[20]))*0.01,
                  'no2': (ord(s[21])*256 + ord(s[22]))*0.01
                  }

def convert(s):
    if s != None:
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B:
          return {'co2': s[3]*256 + s[4],
                  'voc': s[5]*256 + s[6],
                  'humidity': (s[7]*256 + s[8])*0.1,
                  'temperature': ((s[9]*256 + s[10])-500)*0.1,
                  'pm2.5': s[11]*256 + s[12]
                  }
           
def read_all2():
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
#    rxData = read_data()

#    if rxData != None:
#        print(rxData)
#        if 'on' in rxData:
#            print('ON')
#            print("Received:", rxData)

    value = read_all2()
    print (json.dumps(value))

    #write_data(b"\x11\x02\x01\x00\xEC")
    #s=read_data()
    #print("Received:", s)
    #print (json.dumps(convert(s)))
    #abc_off()
    time.sleep(26)    