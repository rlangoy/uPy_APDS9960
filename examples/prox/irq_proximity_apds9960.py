import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960LITE import APDS9960LITE

# Proximity Gain (PGAIN) values
APDS9960_PGAIN_1X = const(0)
APDS9960_PGAIN_2X = const(1)
APDS9960_PGAIN_4X = const(2)
APDS9960_PGAIN_8X = const(3)

# LED Drive values
APDS9960_LED_DRIVE_100MA  = const(0)
APDS9960_LED_DRIVE_50MA   = const(1)
APDS9960_LED_DRIVE_25MA   = const(2)
APDS9960_LED_DRIVE_12_5MA = const(3)

i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
print("Lite APDS-9960 Proximity test ")

apds9960=APDS9960LITE(i2c)
apds9960.prox.eLEDCurrent   =APDS9960_LED_DRIVE_100MA    
apds9960.prox.eProximityGain=APDS9960_PGAIN_8X   

apds9960.prox.enableProximity()
apds9960.prox.setProximityInterruptThreshold(high=10,low=0,persistance=7)
apds9960.prox.enableProximityInterrupt()

ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

sleep_ms(50)

while True:
    sleep_ms(50)

    if(ProxThPin.value()==0):
        print("proximity:", apds9960.prox.readProximity )
        apds9960.prox.clearInterrupt()  
