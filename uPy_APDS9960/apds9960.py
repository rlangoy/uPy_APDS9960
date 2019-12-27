# License:
#                    GNU GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
#             https://www.gnu.org/licenses/gpl-3.0.html
"""`APDS9960`
====================================================
Driver class for the APDS9960 / GY-9960LLC 
   Supports  proximity detection on esp8266
   Tested on:
       GY-9960LLC - https://www.aliexpress.com/item/32738206621.html?spm=a2g0s.9042311.0.0.27424c4dhr0Uo7
       Node MCU v2
       MicroPython v1.11-613-g8ce69288e       
   Work derived from 
       https://github.com/liske/python-apds9960/blob/master/apds9960

Author(s): Rune Langøy  2019
           Thomas Liske 2017  ( https://github.com/liske/python-apds9960/blob/master/apds9960 )

Licence GNU General Public License v3.0
        https://www.gnu.org/licenses/gpl-3.0.html
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
        self._i2c.writeto_mem(APDS9960_ADDR,reg,bytes((val,)))

    def _readByte(self,reg):
        val = self._i2c.readfrom_mem(APDS9960_ADDR,reg, 1)
        return int.from_bytes(val, 'big', True)

    @property
    def getID(self):
        """Prop: Return the APDS9960_ID deviceID"""
        return self._readByte(APDS9960_ID)

    @property
    def proximityIntLowThreshold(self):
        """Prop: Return the low threshold for proximity interrupts"""
        return self._readByte(APDS9960_REG_PILT)
    
    @proximityIntLowThreshold.setter
    def proximityIntLowThreshold(self,threshold):
        """Sets the low threshold for proximity interrupts.
             : low threshold value for interrupt to trigger
        """  
        self._writeByte(APDS9960_REG_PILT,threshold)

    @property
    def proxIntHighThreshold(self):
        """Returns the high threshold for proximity detection.
        """
        return self._readByte(APDS9960_REG_PIHT)
    
    @proxIntHighThreshold.setter
    def proxIntHighThreshold(self, threshold):
        """Sets the high threshold for proximity detection.
        """
        self._writeByte(APDS9960_REG_PIHT, threshold)

    def setProximityInterruptThreshold(self,high=0,low=20,persistance=4):   
        print("setProximityInterruptThreshold")
        self.proximityIntLowThreshold = low    #APDS9960_PILT
        self.proxIntHighThreshold     = high  #APDS9960_PIHT
    
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
        Returns the device status.
        """
        return self._readByte(0x92)

    def setProximityGain(self, gain):
        """Returns receiver gain for proximity detection.
            Value    Gain
              0       1x
              1       2x
              2       4x
              3       8x
            Args:
                gain (int/enum) APDS9960_PGAIN_xx: value for the proximity gain
        """
        val=self._readByte(APDS9960_REG_CONTROL)
        # set bits in register to given value
        gain &= 0b00000011
        gain = gain << 2
        val &= 0b11110011
        val |= gain

        #i2c.writeto_mem(APDS9960_ADDR,APDS9960_REG_CONTROL,bytes((val,)))
        self._writeByte(APDS9960_REG_CONTROL,val)

    def setLEDCurrent(self, eCurent):
        """Sets LED current  for proximity and ALS.
            Value    LED Current
              0        100 mA
              1         50 mA
              2         25 mA
              3         12.5 mA
            Args:
                eCurrent (int/enum): APDS9960_LED_DRIVE_xx value for the LED current 
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
            Args:
                enable (bool): True to enable interrupts, False to turn them off
        """
        val = self._readByte(APDS9960_REG_ENABLE)

        # set bits in register to given value
        val &= 0b11011111;
        if enable:
            val |= 0b00100001  #ensure power on and PIEN

        self._writeByte(APDS9960_REG_ENABLE,val)

    def getMode(self):
        """Returns the mode-enable register (APDS9960_REG_ENABLE) values
        """
        return self._readByte(APDS9960_REG_ENABLE)

    def setMode(self, mode, enable=True):
        """Sets the mode-enable register (APDS9960_REG_ENABLE) values
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
            Args:
                interrupts (bool): True to enable interrupts, False to turn them off
        """
        self.setProximityGain(self._APDS9960_DEFAULT_PGAIN)
        self.setLEDCurrent(self._APDS9960_DEFAULT_LDRIVE)
        self.setProximityIntEnable(interrupts)
        
        self.setMode(APDS9960_MODE_PROXIMITY, True) #enable proximity
        self.setMode(APDS9960_MODE_PROXIMITY_INT, True)
        self.enablePower()

    @property
    def readProximity(self):
        """Reads the APDS9960 proximity level (0 to 255 )
        """               
        return self._readByte(APDS9960_REG_PDATA)
  
    def clearProximityInt(self):
        self._readByte(0xE5)#(APDS9960_PICLEAR)

    def setProxGainCompEnable(self):
        #self.setVal(APDS9960_CONFIG3,0x1,5,val)
        val = self._readByte(0x9F)
        val |= 0b00100000
        self._writeByte(0x9F,val)


    def writeDef(self):
        self._writeByte(0x80,0x25)     # PIEN,PEN,PON
        self._writeByte(0x89 ,0x0);  ##->> Proximity low threshold
        self._writeByte(0x8B ,0x14); ## ->>Proximity high threshold 
        self._writeByte(0x8C ,0x14);  ## ->>Persistance
