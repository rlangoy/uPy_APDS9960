import machine
from time import sleep_ms
from uPy_APDS9960.apdsS9960LITE import APDS9960LITE

#Init I2C Buss
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

apds9960=APDS9960LITE(i2c)         # Enable sensor
print("Enable light Sensor")

apds9960.als.enableSensor()   # Enable Light sensor
apds9960.als.eLightGain=3          # x64 gain
#apds9960.prox.enableProximity()
sleep_ms(50)
print("Clear Light level: ", apds9960.als.ambientLightLevel)
print("Red   Light level: "  , apds9960.als.redLightLevel)
print("Green Light level: ", apds9960.als.greenLightLevel)
print("Blue  Light level: " , apds9960.als.blueLightLevel)

