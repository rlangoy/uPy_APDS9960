import machine
from time import sleep_ms
from uPy_APDS9900.apds9900LITE import APDS9900LITE

#Init I2C Buss NodeMcu
#i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
#Init I2C Buss
i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))

apds9900=APDS9900LITE(i2c)         # Enable sensor
print("Enable light Sensor")

apds9900.als.enableSensor()   # Enable Light sensor
apds9900.als.eLightGain=3          # x64 gain
#apds9900.prox.enableProximity()
sleep_ms(50)
print("Clear Light level: ", apds9900.als.ambientLightLevel)

