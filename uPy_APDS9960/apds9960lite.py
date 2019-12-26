import machine
from time import sleep,sleep_ms
APDS9960_ADDR        = const(0x39)

class APDS9960LITE :
    """
    APDS9960 low memory driver that provides proximity driver services for  ASDS9960 with Device ID:  0xa8 
    """
    def __init__(self,
                i2c):
        
        self._i2c=i2c
        self._writeByte(0x80,0) # APDS9960_ENABLE PON=0
        sleep_ms(50)
        self._writeByte(0x80,0b00000001) # APDS9960_ENABLE PON=1
 
    def _writeByte(self,reg,val):
        self._i2c.writeto_mem(APDS9960_ADDR,reg,bytes((val,)))

    def _readByte(self,reg):
        val =self._i2c.readfrom_mem(APDS9960_ADDR,reg, 1)
        return int.from_bytes(val, 'big', True)

        
    def enableProximity(self,on=True):
         # PEN - bit 2
        val=self._readByte(0x80)   # Get reg APDS9960_ENABLE
        if on == True:
            val=val | (1<<2)  # APDS9960_ENABLE 
        else:
            val=val & ~(1<<2) # APDS9960_ENABLE )
        
        self._writeByte(0x80,val) #write APDS9960_ENABLE

    def setProximityInterruptThreshold(self,high=0,low=20,persistance=4):   
        self._writeByte(0x89, low);   #APDS9960_PILT
        self._writeByte(0x8B, high);  #APDS9960_PIHT
        
        if (persistance>7) :
            persistance=7

        val=self._readByte(0x8C) #APDS9960_PERS 0x8C<7:4>  Proximity Interrupt Persistence 
        val=val & 0b00011111          # Clear PERS
        val=val | (persistance << 4)  # Set   PERS
        self._writeByte(0x8C,val) # Update APDS9960_PERS
        
    def clearInterrupt(self):
         self._writeByte(0xE7,0) #  APDS9960_AICLEAR clear all interrupts
         self._readByte(0xE5)#(APDS9960_PICLEAR)
     
    def enableProximityInterrupt(self,on=True):
        val=self._readByte(0x80)      # Read APDS9960_ENABLE
        if on == True:
            val=val | (1<<5)     # APDS9960_ENABLE   (PIEN -bit 5)
        else:
            val=val & ~(1<<5)    # APDS9960_ENABLE )
        
        self._writeByte(0x80,val)     # write APDS9960_ENABLE
        self.clearInterrupt(); 

    def readProximity(self):
            """Reads the APDS9960 proximity level (0 to 255 )
            """               
            return self._readByte(0x9c)
        
    def statusRegister(self):
            """
            Status Register (0x93)
            The read-only Status Register provides the status of the device. The register is set to 0x04 at power-up.
            Returns the device status.
            """
            return self._readByte(0x92)

    def writeDef(self):
             self._writeByte(0x80,0x25)     # PIEN,PEN,PON
    #          _writeByte(0x89 ,0x0);  ##->> Proximity low threshold
    #          _writeByte(0x8B ,0x14); ## ->>Proximity high threshold 
    #          _writeByte(0x8C ,0x14);  ## ->>Persistance
    #         _writeByte(0x8E ,0x40);
     #       _writeByte(0x8F ,0x00);
    #         _writeByte(0x90 ,0x01);
    #         _writeByte(0x93 ,0x02);
    #         _writeByte(0x9C ,0x10);
    #         _writeByte(0x9D ,0x00);
     #       _writeByte(0x9E ,0x00);
     #       _writeByte(0x9F ,0x00);       


if __name__ == '__main__':

    i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    print("Lite APDS-9960 Proximity test ")

    proxSensor=APDS9960LITE(i2c)
    proxSensor.enableProximity()
    proxSensor.setProximityInterruptThreshold(high=10,low=0,persistance=7)
    proxSensor.enableProximityInterrupt()

    ProxThPin=machine.Pin(0, machine.Pin.IN ,machine.Pin.PULL_UP)

    sleep(.1)

    while True:
        sleep_ms(50)
        
        if(ProxThPin.value()==0):
            print("proximity:", proxSensor.readProximity() )
            proxSensor.clearInterrupt()  #one more time
               
