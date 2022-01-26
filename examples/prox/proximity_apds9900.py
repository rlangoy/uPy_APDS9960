import machine
from time import sleep_ms
from uPy_APDS9900.apds9900LITE import APDS9900LITE

# Proximity Gain (PGAIN) values
APDS9900_PGAIN_1X = const(0)
APDS9900_PGAIN_2X = const(1)
APDS9900_PGAIN_4X = const(2)
APDS9900_PGAIN_8X = const(3)

# LED Drive values
APDS9900_LED_DRIVE_100MA  = const(0)
APDS9900_LED_DRIVE_50MA   = const(1)
APDS9900_LED_DRIVE_25MA   = const(2)
APDS9900_LED_DRIVE_12_5MA = const(3)

#Init I2C Buss NodeMcu
#i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
#Init I2C Buss Micropython
i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))


APDS9900=APDS9900LITE(i2c)
APDS9900.prox.eLEDCurrent   =APDS9900_LED_DRIVE_100MA    
APDS9900.prox.eProximityGain=APDS9900_PGAIN_8X   
APDS9900.prox.enableSensor()

sleep_ms(50)

while True:
    sleep_ms(50)
    print("proximity:", APDS9900.prox.proximityLevel )
