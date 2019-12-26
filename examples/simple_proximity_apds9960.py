import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960 import APDS9960

#Init I2C Buss
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

proxSensor=APDS9960(i2c)              # Enable sensor
proxSensor.enableProximitySensor()    # Enable Proximit sensing

while True:
        sleep_ms(25) # wait for readout to be ready
        print(proxSensor.readProximity)   #Print the proximity value