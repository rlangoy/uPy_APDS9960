import machine
from time import sleep_ms
from uPy_APDS9960.apds9960LITE import APDS9960LITE

i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

apds9960=APDS9960LITE(i2c)
apds9960.prox.eLEDCurrent    =0 # LED_DRIVE_100MA    
apds9960.prox.eProximityGain =3 # PGAIN_8X   
apds9960.prox.enableSensor()

#IRQ Functionalities
apds9960.prox.setInterruptThreshold(high=10,low=0,persistance=7)
apds9960.prox.enableInterrupt()

ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

sleep_ms(50)

while True:
    sleep_ms(50)

    if(ProxThPin.value()==0):
        print("proximity:", apds9960.prox.proximityLevel )
        apds9960.prox.clearInterrupt()  
