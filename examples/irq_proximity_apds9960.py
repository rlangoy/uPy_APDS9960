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

print("Starting APDS9960 Poximity test prog")
print("------------------------------------")
print("Proximity test SCL->Pin5  and SDA -> Pin 4 ")
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
proxSensor=APDS9960(i2c,
                    debug=True,
                    photoGain = APDS9960_PGAIN_8X,
                    ledCurrent = APDS9960_LED_DRIVE_12_5MA)    
print("Set prx-threshold")
proxSensor.setProximityInterruptThreshold(high=10,low=0,persistance=2)
print("proxSensor.enableProximitySensor()")
proxSensor.enableProximitySensor()
    
# Int pin from the APDS9960 breakoutboard connected to pin 0
ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

# Blue-led mouynted on ESP8266 Module
led = machine.Pin(2, machine.Pin.OUT)
led.value(1) # Turn led off
sleep_ms(50)

while True:
    led.value(ProxThPin.value())
    if(ProxThPin.value()==0):
        print(proxSensor.readProximity )
        proxSensor.clearProximityInt()