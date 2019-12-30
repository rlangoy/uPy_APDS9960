"""`APDS9960LITE`
====================================================

Low memory Driver class for the APDS9960 

    Author: Rune Langøy  2019
 
    Licence GNU General Public License v3.0
    https://www.gnu.org/licenses/gpl-3.0.html
"""
from time import sleep
from micropython import const
#APDS9960_ADDR        = const(0x39)

class I2CEX:
    """micropython i2c adds functions for reading / writing byte to a register 

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    """

    def __init__(self,
                 i2c, 
                 address):
        self.__i2c=i2c
        self.__address=address
    def __regWriteBit(self,reg,bitPos,bitVal)
        """Writes a I2C byte to the address APDS9960_ADDR (0x39)

            :param reg: The I2C register that is writen to
            :type reg: int

            :param bitPos: The bit position (0 - 7)
            :type bitPos: int        
            
            :param value: True = set-bit / False =clear bit
            :type value: bool        
        """
        val=this.__readByte(reg)   # read reg 
        if bitVal == True:
            val=val | (1<<bitPos)  # set bit
        else:
            val=val & ~(1<<bitPos) # clear bit
        
        super().__writeByte(reg,val) #write reg
  
    
    def __writeByte(self,reg,val):
        """Writes a I2C byte to the address APDS9960_ADDR (0x39)

            :param reg: The I2C register that is writen to
            :type reg: int
            :param val: The I2C value to write in the range (0- 255)
            :type val: int        
        """
        self.__i2c.writeto_mem(self.__address,reg,bytes((val,)))

    def __readByte(self,reg):
        """Reads a I2C byte from the address APDS9960_ADDR (0x39)

        :param reg: The I2C register to read
        :type reg: int

        :param val: The I2C value to write in the range (0- 255)
        :type val: int 

        :returns: a value in the range (0- 255)
        :rtype: int      
        """

        val =self.__i2c.readfrom_mem(self.__address,reg, 1)
        return int.from_bytes(val, 'big', True)
    

class PROX(I2CEX) :
    """APDS9960 proximity functons   

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    """    
    def __init__(self,
                 i2c):
        super().__init__(i2c,0x39) # initiate I2CEX with APDS9960_ADDR
        
    def enableProximity(self,on=True):
        """Enable/Disable the proimity sensor

        :param on: Enables / Disables the proximity sensor
                (Default True)
        :type on: bool
        """
         # PEN - bit 2
        val=super().__readByte(0x80)   # Get reg APDS9960_ENABLE
        if on == True:
            val=val | (1<<2)  # APDS9960_ENABLE 
        else:
            val=val & ~(1<<2) # APDS9960_ENABLE )
        
        super().__writeByte(0x80,val) #write APDS9960_ENABLE

    def setProximityInterruptThreshold(self,high=0,low=20,persistance=4):
        """Enable/Disable the proimity sensor

        :param high: high level for generating proximity hardware interrupt (Range 0 - 255)
        :type high: int 

        :param low: low level for generating proximity hardware interrupt (Range 0 - 255)
        :type low: int 

        :param persistance: Number of consecutive reads before IRQ is raised (Range 0 - 7)
        :type persistance: int 

        """   
        super().__writeByte(0x89, low);   #APDS9960_PILT
        super().__writeByte(0x8B, high);  #APDS9960_PIHT
        
        if (persistance>7) :
            persistance=7

        val=super().__readByte(0x8C) #APDS9960_PERS 0x8C<7:4>  Proximity Interrupt Persistence 
        val=val & 0b00011111          # Clear PERS
        val=val | (persistance << 4)  # Set   PERS
        super().__writeByte(0x8C,val) # Update APDS9960_PERS
        
    def clearInterrupt(self):
        """Crears the proimity interrupt
        IRQ HW output goes low (enables triggering of new IRQ)
        """
        super().__writeByte(0xE7,0) #  APDS9960_AICLEAR clear all interrupts
        super().__readByte(0xE5)#(APDS9960_PICLEAR)
     
    def enableProximityInterrupt(self,on=True):
        """Enables/Disables IRQ dependent on limits given by setProximityInterruptThreshold()

        :param on: Enable / Disable Hardware IRQ  
        :type on: bool 
        """
        val=super().__readByte(0x80)      # Read APDS9960_ENABLE
        if on == True:
            val=val | (1<<5)     # APDS9960_ENABLE   (PIEN -bit 5)
        else:
            val=val & ~(1<<5)    # APDS9960_ENABLE )
        
        super().__writeByte(0x80,val)     # write APDS9960_ENABLE
        self.clearInterrupt(); 

    def readProximity(self):
            """Reads the APDS9960 proximity level 

            :returns: proximity as a value in the range (0- 255)
            :rtype: int      
            """               
            return super().__readByte(0x9c)
    

class APDS9960LITE(I2CEX) :
    """APDS9960LITE low memory driver for ASDS9960  

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    
    :example:
      .. code:: python

        import machine 
        from uPy_APDS9960.APDS9960LITE import APDS9960LITE
        
        i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))  # Creates I2C Driver on Pin 5 / 6
        adps9960=APDS9960LITE(i2c)                                  # Create APDS9960 Driver
        #adps9960.prox  <- (PROX) Provides proximity functionalities
    """
    def __init__(self,
                i2c):      
        """Construct the APDS9960 driver class 

        :param i2c: The I2C driver
        :type i2C: machine.i2c
        """
        super().__init__(i2c,0x39) # initiate I2CEX with APDS9960_ADDR

        super().__writeByte(0x80,0) # APDS9960_ENABLE PON=0
        sleep(.05)
        super().__writeByte(0x80,0b00000001) # APDS9960_ENABLE PON=1
        self.prox=PROX(i2c)
        
    prox = None
    """APDS9960 Proximity functions :class:`.PROX`"""

    def statusRegister(self):
            """
            Status Register (0x93)
            The read-only Status Register provides the status of the device. The register is set to 0x04 at power-up.
            Returns the device status.

            :returns: Status register content 

            ::

              PGSAT - bit6 - Proximity Saturation
              PINT  - bit5 - Proximity Interrupt
              PVALID- bit1 - Proximity Valid 

            :rtype: int      
            """
            return super().__readByte(0x93)


    
