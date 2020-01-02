import machine
from time import sleep_ms
from uPy_APDS9960.APDS9960LITE import APDS9960LITE

#Init I2C Buss
i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

apds9960=APDS9960LITE(i2c)         # Enable sensor
apds9960.als.enableLightSensor()   # Enable Light sensor
apds9960.als.eLightGain=3          # x64 gain
apds9960.als.setLightInterruptThreshold(high=100,low=0,persistance=7)
apds9960.als.enableInterrupt(True)     # Enable interrupt
apds9960.als.clearInterrupt()          # Clear interrupt
sleep_ms(50)

IrqThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)
sleep_ms(50)

while True:
    sleep_ms(50)

    if(IrqThPin.value()==0):
        print("Ambient light level:", apds9960.als.ambientLightLevel )
        apds9960.als.clearInterrupt()
