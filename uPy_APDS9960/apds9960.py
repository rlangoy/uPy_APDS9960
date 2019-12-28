# License:
#                    GNU GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
#             https://www.gnu.org/licenses/gpl-3.0.html
"""
`APDS9960`
====================================================

|    Driver class for the APDS9960 / GY-9960LLC 
|    Supports  proximity detection on esp8266
|    Tested on:
|       GY-9960LLC - https://www.aliexpress.com/item/32738206621.html?spm=a2g0s.9042311.0.0.27424c4dhr0Uo7
|       Node MCU v2
|       MicroPython v1.11-613-g8ce69288e       
|    Work derived from 
|      https://github.com/liske/python-apds9960/blob/master/apds9960
|
|    Author(s): 
|       Rune Langøy  2019
|       Thomas Liske 2017  ( https://github.com/liske/python-apds9960/blob/master/apds9960 )
|
|    Licence GNU General Public License v3.0
|    https://www.gnu.org/licenses/gpl-3.0.html
"""
from time import sleep
from micropython import const


__version__ = "0.1.0-auto.0"
__repo__ = "https://github.com/rlangoy/uPy_APDS9960.git"

#pylint: enable-msg=bad-whitespace
APDS9960_ADDR        = const(0x39)

# APDS9960 register addresses
APDS9960_REG_ENABLE  = const(0x80)
APDS9960_REG_PDATA   = const(0x9c)
APDS9960_ID          = const(0x92)
APDS9960_REG_PILT    = const(0x89)
APDS9960_REG_PIHT    = const(0x8b)
APDS9960_REG_CONTROL = const(0x8f)

# Proximity Gain (PGAIN) values
APDS9960_PGAIN_1X = const(0)
APDS9960_PGAIN_2X = const(1)
APDS9960_PGAIN_4X = const(2)
APDS9960_PGAIN_8X = const(3)

# LED Drive values
APDS9960_LED_DRIVE_100MA = const(0)
APDS9960_LED_DRIVE_50MA = const(1)
APDS9960_LED_DRIVE_25MA = const(2)
APDS9960_LED_DRIVE_12_5MA = const(3)

# APDS9960 modes
APDS9960_MODE_POWER = const(0)
APDS9960_MODE_ALL   = const(7)
APDS9960_MODE_PROXIMITY = const(2)
APDS9960_MODE_PROXIMITY_INT = const(5)

#pylint: disable-msg=too-many-instance-attributes
class APDS9960 :
    """
      APDS9960 provide proximity driver services for  ASDS9960 with Device ID:  0xa8 

    :param i2c: The I2C driver
    :type i2C: machine.i2c
    :param address: The APDS9960 I2C address (default 0x39)
    :type address: int
    :param debug: Enable/disable debug messages 
    :type debug: bool
    :param photoGain: Photo detector gain (1x,2x,4x,8x)
    :type photoGain: int
    :param ledCurrent: led current (100mA,50mA,25mA,12.5mA)
    :type ledCurrent: iny
    
    :example:
      .. code:: python

        import machine
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
    """
    def __init__(self,
                 i2c, 
                 address=APDS9960_ADDR,
                 debug=False,
                 photoGain = APDS9960_PGAIN_4X,
                 ledCurrent = APDS9960_LED_DRIVE_12_5MA):
        self._i2c=i2c
        self._debug=debug
        self._APDS9960_DEFAULT_PGAIN=photoGain
        self._APDS9960_DEFAULT_LDRIVE=ledCurrent
        self.proximityIntLowThreshold = 0
        self.proxIntHighThreshold = 50
        
        self._writeByte(0x8C,0)       
        self._writeByte(APDS9960_REG_ENABLE,0) #power off
        sleep(.03)
        self._writeByte(APDS9960_REG_ENABLE,0b00100101) #Power on
        
        #If Debug mode exit now :)
        if (debug==False):
            return
        
        print('Scan i2c bus...')
        devices = i2c.scan()
        #chk if i2c devices found
        if len(devices) == 0:
          print("Error:\n No i2c device !")
          raise RuntimeError()

        print('i2c devices found:',len(devices))
     
        for device in devices:  
           print("Decimal address: ",device," | Hex address: ",hex(device))
        
        #chk if APDS9960 is present
        if(device!=address):
           print("Error:\n No APDS9960 found !")
           raise RuntimeError()
        
        print("Device ID: ",hex(self.getID))
        
    def _writeByte(self,reg,val):
        """Writes a I2C byte to the address APDS9960_ADDR (0x39)

            :param reg: The I2C register that is writen to
            :type reg: int
            :param val: The I2C value to write in the range (0- 255)
            :type val: int        
        """
        self._i2c.writeto_mem(APDS9960_ADDR,reg,bytes((val,)))

    def _readByte(self,reg):
        """Reads a I2C byte from the address APDS9960_ADDR (0x39)

        :param reg: The I2C register to read
        :type reg: int

        :param val: The I2C value to write in the range (0- 255)
        :type val: int 

        :returns: a value in the range (0- 255)
        :rtype: int      
        """

        val =self._i2c.readfrom_mem(APDS9960_ADDR,reg, 1)
        return int.from_bytes(val, 'big', True)

    @property
    def getID(self):
        """ APDS9960 chip deviceID 

            :getter: Returns the deviceID 
            :type: int     
        """        
        return self._readByte(APDS9960_ID)

    @property
    def proximityIntLowThreshold(self):
        """Low threshold for proximity interrupts
        
            :getter: Returns low threshold value (0-255)
            :setter: Sets the low threshold value (0-255)
            :type: int
        """
        return self._readByte(APDS9960_REG_PILT)
    
    @proximityIntLowThreshold.setter
    def proximityIntLowThreshold(self,threshold):
        self._writeByte(APDS9960_REG_PILT,threshold)

    @property
    def proxIntHighThreshold(self):
        """Hihg threshold for proximity interrupts
        
            :getter: Returns high threshold value (0-255)
            :setter: Sets the ighlow threshold value (0-255)
            :type: int
        """

        return self._readByte(APDS9960_REG_PIHT)
    
    @proxIntHighThreshold.setter
    def proxIntHighThreshold(self, threshold):
        self._writeByte(APDS9960_REG_PIHT, threshold)

    def setProximityInterruptThreshold(self,high=0,low=20,persistance=4): 

        self.proximityIntLowThreshold = low    #writes to reg: APDS9960_PILT
        self.proxIntHighThreshold     = high   #writes to reg:APDS9960_PIHT
    
        if (persistance>7) :
            persistance=7

        val=self._readByte(0x8C) #APDS9960_PERS 0x8C<7:4>  Proximity Interrupt Persistence 
        val=val & 0b00011111          # Clear PERS
        val=val | (persistance << 4)  # Set   PERS
        self._writeByte(0x8C,val) # Update APDS9960_PERS

    @property
    def statusRegister(self):
        """
        Status Register (0x93)
        The read-only Status Register provides the status of the device. The register is set to 0x04 at power-up.

        :returns: Status register content: 

        ::

             PGSAT - bit6 - Proximity Saturation
             PINT  - bit5 - Proximity Interrupt
             PVALID- bit1 - Proximity Valid 

        :rtype: int      
        """
        return self._readByte(0x92)

    def setProximityGain(self, eGain):
        """Sets the receiver gain for proximity detection.
        
        :param eGain: the reciever gain (0 -3)
        :type geGainain: int
     
        ::

            eGain    Gain
              0       1x
              1       2x
              2       4x
              3       8x
        """
        val=self._readByte(APDS9960_REG_CONTROL)
        # set bits in register to given value
        eGain &= 0b00000011
        eGain = eGain << 2
        val &= 0b11110011
        val |= eGain

        #i2c.writeto_mem(APDS9960_ADDR,APDS9960_REG_CONTROL,bytes((val,)))
        self._writeByte(APDS9960_REG_CONTROL,val)

    def setLEDCurrent(self, eCurent):
        """
        Sets LED current for proximity and ALS.

        :param eCurent: the LED current (0 -3)
        :type eCurent: int

        ::

          eCurent  LED Current
            0        100 mA
            1         50 mA
            2         25 mA
            3         12.5 mA
        """
        val=self._readByte(APDS9960_REG_CONTROL)        
        
        # set bits in register to given value
        eCurent &= 0b00000011
        eCurent = eCurent << 6
        val &= 0b00111111
        val |= eCurent

        self._writeByte(APDS9960_REG_CONTROL,val)

    def setProximityIntEnable(self, enable):
        """Turns proximity interrupts on or off.
    
        :param enable: True to enable interrupts, False to turn them off
        :type enable: bool
        """
        val = self._readByte(APDS9960_REG_ENABLE)

        # set bits in register to given value
        val &= 0b11011111;
        if enable:
            val |= 0b00100001  #ensure power on and PIEN

        self._writeByte(APDS9960_REG_ENABLE,val)

    def getMode(self):
        """Returns the APDS9960 mode-enable register value

        :returns: The APDS9960_REG_ENABLE register value (0- 255)
        :rtype: int      
        """
        return self._readByte(APDS9960_REG_ENABLE)

    def setMode(self, mode, enable=True):
        """Sets the mode-enable register (APDS9960_REG_ENABLE) values

        :param mode: bit to set/clear  (value 0 - 7 )
        :type mode: int      
        :param enable: True to set the mode bit, False to clear the mode bit
        :type enable: bool
   
        """
        reg_val = self.getMode()

        if mode < 0 or mode > APDS9960_MODE_ALL:
            raise ADPS9960InvalidMode(mode)

        # change bit(s) in ENABLE register */
        if mode == APDS9960_MODE_ALL:
            if enable:
                reg_val = 0x7f
            else:
                reg_val = 0x00
        else:
            if enable:
                reg_val |= (1 << mode);
            else:
                reg_val &= ~(1 << mode);

        # write value to ENABLE register
        self._writeByte(APDS9960_REG_ENABLE,reg_val)
    
    def enablePower(self):
        """Power on APDS-9960
        """        
        self.setMode(APDS9960_MODE_POWER, True)


    def disablePower(self):
        """Power off APDS-9960
        """        
        self.setMode(APDS9960_MODE_POWER, False)

    # start the proximity sensor
    def enableProximitySensor(self, interrupts=True):
        """Turns proximity messuremtnt on 

        :param interrupts: true to enable interrupts, False to turn it off
        :type interrupts: bool
        """
        self.setProximityGain(self._APDS9960_DEFAULT_PGAIN)
        self.setLEDCurrent(self._APDS9960_DEFAULT_LDRIVE)
        self.setProximityIntEnable(interrupts)
        
        self.setMode(APDS9960_MODE_PROXIMITY, True) #enable proximity
        self.setMode(APDS9960_MODE_PROXIMITY_INT, True)
        self.enablePower()

    @property
    def readProximity(self):
        """Reads the APDS9960 proximity level

            :getter: Returns the proximity level (0 - 255 ) 
            :type: int     
        """        
        return self._readByte(APDS9960_REG_PDATA)
  
    def clearProximityInt(self):
        """Crears the proimity interrupt
        IRQ HW output goes low (enables triggering of new IRQ)
        """
        self._readByte(0xE5)#(APDS9960_PICLEAR)