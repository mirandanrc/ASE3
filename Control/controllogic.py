import machine
import utime


#Motor 1 delante izquierdo
PUL = 1  # Pin para la señal de pulso
DIR = 0  # Define el pin de dirección
#Motor 2 delante derecho
PUL2 = 3
DIR2 = 2
#Motor 3 trasero izquierdo
PUL3 = 5
DIR3 = 4
#Motor 4 trasero derecho
PUL4 = 7
DIR4 = 6

#Motor 1
pul_pin = machine.Pin(PUL, machine.Pin.OUT)
dir_pin = machine.Pin(DIR, machine.Pin.OUT)

#Motor 2
pul_pin2 = machine.Pin(PUL2, machine.Pin.OUT)
dir_pin2 = machine.Pin(DIR2, machine.Pin.OUT)

#Motor 3
pul_pin3 = machine.Pin(PUL3, machine.Pin.OUT)
dir_pin3 = machine.Pin(DIR3, machine.Pin.OUT)

#Motor 4
pul_pin4 = machine.Pin(PUL4, machine.Pin.OUT)
dir_pin4 = machine.Pin(DIR4, machine.Pin.OUT)

def RevMotor1():
    # Reversa Motor 1
    dir_pin.value(0)
    for i in range(1600):  # 1600 pasos
        pul_pin.value(1)
        utime.sleep_us(400)
        pul_pin.value(0)
        utime.sleep_us(400)

def RevMotor2():
    # Reversa Motor 3
    dir_pin2.value(1)
    for i in range(1600):  # 1600 pasos
        pul_pin2.value(1)
        utime.sleep_us(400)
        pul_pin2.value(0)
        utime.sleep_us(400)

def RevMotor3():
    # Reversa Motor 3
    dir_pin3.value(1)
    for i in range(1600):  # 1600 pasos
        pul_pin3.value(1)
        utime.sleep_us(400)
        pul_pin3.value(0)
        utime.sleep_us(400)

def RevMotor4():
    # Reversa Motor 3
    dir_pin4.value(0)
    for i in range(1600):  # 1600 pasos
        pul_pin4.value(1)
        utime.sleep_us(400)
        pul_pin4.value(0)
        utime.sleep_us(400)

def Reversa():
    dir_pin.value(0)
    dir_pin2.value(1)
    dir_pin3.value(1)
    dir_pin4.value(0)
    for i in range(1600):  # 1600 pasos
        pul_pin.value(1)
        pul_pin2.value(1)
        pul_pin3.value(1)
        pul_pin4.value(1)
        utime.sleep_us(400)
        pul_pin.value(0)
        pul_pin2.value(0)
        pul_pin3.value(0)
        pul_pin4.value(0)
        utime.sleep_us(400)
        
def AdeMotor1():
    # Adelante Motor 1
    dir_pin.value(1)
    for i in range(1600):  # 1600 pasos
        pul_pin.value(1)
        utime.sleep_us(400)
        pul_pin.value(0)
        utime.sleep_us(400)

def AdeMotor2():
    # Adelante Motor 2
    dir_pin2.value(0)
    for i in range(1600):  # 1600 pasos
        pul_pin2.value(1)
        utime.sleep_us(400)
        pul_pin2.value(0)
        utime.sleep_us(400)
        
def AdeMotor3():
    # Adelante Motor 2
    dir_pin3.value(0)
    for i in range(1600):  # 1600 pasos
        pul_pin3.value(1)
        utime.sleep_us(400)
        pul_pin3.value(0)
        utime.sleep_us(400)
        
def AdeMotor4():
    # Adelante Motor 2
    dir_pin4.value(1)
    for i in range(1600):  # 1600 pasos
        pul_pin4.value(1)
        utime.sleep_us(400)
        pul_pin4.value(0)
        utime.sleep_us(400)
        
def Adelante():
    dir_pin.value(1)
    dir_pin2.value(0)
    dir_pin3.value(0)
    dir_pin4.value(1)
    for i in range(1600):  # 1600 pasos
        pul_pin.value(1)
        pul_pin2.value(1)
        pul_pin3.value(1)
        pul_pin4.value(1)
        utime.sleep_us(400)
        pul_pin.value(0)
        pul_pin2.value(0)
        pul_pin3.value(0)
        pul_pin4.value(0)
        utime.sleep_us(400)
        
def Para():
    pul_pin.value(0)
    
while True:
    RevMotor1()
    utime.sleep(0.1)
    RevMotor2()
    utime.sleep(0.1)
    RevMotor3()
    utime.sleep(0.1)
    RevMotor4()
    utime.sleep(0.1)
    Reversa()
    utime.sleep(0.1)
    
    AdeMotor1()
    utime.sleep(0.1)
    AdeMotor2()
    utime.sleep(0.1)
    AdeMotor3()
    utime.sleep(0.1)
    AdeMotor4()
    utime.sleep(0.1)
    Adelante()
    utime.sleep(0.1)
    
    Para()
    utime.sleep(2)