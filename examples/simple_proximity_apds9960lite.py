import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960LITE import APDS9960LITE
    
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
print("Lite APDS-9960 Proximity test ")

proxSensor=APDS9960LITE(i2c)
proxSensor.enableProximity()
proxSensor.setProximityInterruptThreshold(high=10,low=0,persistance=7)
proxSensor.enableProximityInterrupt()

ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

sleep_ms(50)

while True:
    sleep_ms(50)

    if(ProxThPin.value()==0):
        print("proximity:", proxSensor.readProximity() )
        proxSensor.clearInterrupt()  #one more time
