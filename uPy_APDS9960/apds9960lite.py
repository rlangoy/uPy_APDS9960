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
