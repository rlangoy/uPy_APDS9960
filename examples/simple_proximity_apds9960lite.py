import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960LITE import APDS9960LITE
    
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
print("Lite APDS-9960 Proximity test ")

apds9960=APDS9960LITE(i2c)
apds9960.prox.enableProximity()
apds9960.prox.setProximityInterruptThreshold(high=10,low=0,persistance=7)
apds9960.prox.enableProximityInterrupt()
apds9960.prox.eLEDCurrent=3     #100 mA (max)
apds9960.prox.eProximityGain=3  #gain x8 (max)


print("eProximityGain", apds9960.prox.eProximityGain)
print("eLEDCurrent ",apds9960.prox.eLEDCurrent )


ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

sleep_ms(50)

#while True:
#    sleep_ms(50)
#
#    if(ProxThPin.value()==0):
#        print("proximity:", apds9960.prox.readProximity() )
#        apds9960.prox.clearInterrupt()  #one more time
