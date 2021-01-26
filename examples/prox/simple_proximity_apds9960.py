import machine
from time import sleep_ms
from uPy_APDS9960.apds9960LITE import APDS9960LITE

#Init I2C Buss
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

apds9960=APDS9960LITE(i2c)      # Enable sensor
apds9960.prox.enableSensor()    # Enable Proximit sensing

while True:
        sleep_ms(25) # wait for readout to be ready
        print(apds9960.prox.proximityLevel)   #Print the proximity value
