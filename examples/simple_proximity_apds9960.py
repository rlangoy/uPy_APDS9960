import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960LITE import APDS9960LITE

#Init I2C Buss
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

apds9960=APDS9960LITE(i2c)         # Enable sensor
apds9960.prox.enableProximity()    # Enable Proximit sensing
apds9960.als.enableLightSensor()   # Enable Light sensor 
while True:
        sleep_ms(25) # wait for readout to be ready
        print(apds9960.prox.readProximity)   #Print the proximity value