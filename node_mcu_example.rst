NodeMCU & MicroPython APDS-9960 example
=======================================



Usage Example
=============

.. code-block:: python

  import machine
  from time import sleep_ms
  from uPy_APDS9960.apds9960LITE import APDS9960LITE

  #Init I2C Buss
  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

  apds9960=APDS9960LITE(i2c)      # Enable sensor
  apds9960.prox.enableSensor()    # Enable Proximit sensing

  while True:
          sleep_ms(25) # wait for readout to be ready
          print(apds9960.prox.proximityLevel)   #Print the proximity value


Hardware Set-up
---------------

Connect Vin to 3.3 V or 5 V power source, GND to ground, SCL and SDA to the appropriate pins to the NooeMCU Devboard

========== ====== ============ ======== ==============
APDS9960   Name   Remarks      NodeMcu  Pin  Function  
========== ====== ============ ======== ==============
1           VIN    +3.3V Power  3V3      +3.3V Power           
2           GND    Ground       GND      GND           
3           SCL    I2C clock    D1       GPIO 5 (SCL)   
4           SDA    I2C Data     D2       GPIO 4 (SDA)   
5           INT    Interrupt    D3       GPIO 0   
========== ====== ============ ======== ==============

.. raw:: html

    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images//APDS9960hookup.PNG">

Basics
------

Of course, you must import the device and library :)

.. code:: python

  import machine
  from uPy_APDS9960.apds9960LITE import APDS9960LITE
 

To set-up the device to gather data, initialize the I2C-device using SCL and SDA pins. 
Then initialize the library.  

.. code:: python

  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
  apds9960=APDS9960LITE(i2c)         # Poweron APDS9960
  

Proximity
~~~~~~~~~
Proximity funxtionalites is accessed torough the apds9960.prox member :class:`.PROX`

.. code:: python

  apds9960.prox.enableSensor()         # Enable Proximity sensing
  sleep_ms(25)                         # wait for readout to be ready
  print(apds9960.prox.proximityLevel)  # Print the proximity value

Light Sensing
~~~~~~~~~~~~~
Proximity funxtionalites is accessed torough the apds9960.als member :class:`.ALS`

.. code:: python

  apds9960.als.enableSensor()           # Enable Light sensor
  sleep_ms(25)                          # Wait for readout to be ready
  print(apds9960.als.ambientLightLevel) # Print the ambient light value