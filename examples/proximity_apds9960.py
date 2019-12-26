import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960 import APDS9960

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
proxSensor=APDS9960(i2c,
                    debug=True,
                    photoGain = APDS9960_PGAIN_8X,
                    ledCurrent = APDS9960_LED_DRIVE_100MA)

proxSensor.enableProximitySensor()

while True:
        sleep_ms(25) # wait for readout to be ready
        print(proxSensor.readProximity)