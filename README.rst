MicroPython APDS-9960 & APDS-9900 RAM optimized Library
=======================================================

.. image:: https://readthedocs.org/projects/upy-apds9960/badge/?version=latest
    :target: https://upy-apds9960.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

|
.. raw:: html 
    
    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images/breakoutboard.jpg">

Another APDS9960 / GY-9960LLC / APDS9900 micro python library optimized for ESP8266 / ESP12-E for:
    * Light Sensing  (Ambient Light and RGB Color Sensing)
    * Proximity Sensing

Documentation 
=============
Complete documentation is hosted on the "Read the Docs" page 
`upy-apds9960.readthedocs.io <https://upy-apds9960.readthedocs.io>`_


Dependencies
============
This driver depends on:

* `MicroPython <http://micropython.org/>`_

Tested on:
      | Sensor:   `GY-9960LLC <https://www.aliexpress.com/item/32738206621.html>`_
      | Sensor:   `APDS-9900  <https://www.aliexpress.com/item/32738206621.html>`_
      | Devboard: Node MCU v1.0 & Raspberry PI Pico

Installation
============
* Flash the device with MicroPython
* Copy the folder uPy_APDS9960 and content (apds9960LITE.py) to the root folder for APDS9960 circuits
* Copy the folder uPy_APDS9900 and content (apds9900LITE.py) to the root folder for APDS9900 circuits

The steps above is descsribed in the `Thonny IDE tutorial`_.

.. _Thonny IDE tutorial: https://upy-apds9960.readthedocs.io/en/latest/thonny_guide.html

Examples
========
The examples in theis respository uses the NodeMCU devboard the devboard to use rpi pico please change the I2C inferface as show in the code below

.. code-block:: python

  #Change I2C interface from: 
  #  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
  #to:
  i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))

Here is the `NodeMCU Hookup`_.

.. _NodeMCU Hookup: ./node_mcu_example.rst

APDS9960 Example
================

.. code-block:: python

  import machine
  from time import sleep_ms
  from uPy_APDS9960.apds9960LITE import APDS9960LITE

  #Init I2C Buss on RP2040
  i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))

  apds9960=APDS9960LITE(i2c)      # Enable sensor
  apds9960.prox.enableSensor()    # Enable Proximit sensing

  while True:
          sleep_ms(25) # wait for readout to be ready
          print(apds9960.prox.proximityLevel)   #Print the proximity value

APDS9900 ESP32-C3 Example
================

.. code-block:: python

    import machine
    from time import sleep_ms
    from uPy_APDS9900.apds9900LITE import APDS9900LITE
    
    #Init Left I2C Buss on ESP32-C3
    i2c =  machine.SoftI2C(scl=machine.Pin(9), sda=machine.Pin(8))
    
    apds9900=APDS9900LITE(i2c)      # Enable sensor
    apds9900.prox.enableSensor()    # Enable Proximit sensing
    
    while True:
            sleep_ms(25) # wait for readout to be ready
            print(apds9900.prox.proximityLevel)   #Print the proximity value


APDS9900 Raspberry Pico Example
================

.. code-block:: python

    import machine
    from time import sleep_ms
    from uPy_APDS9900.apds9900LITE import APDS9900LITE

    #Init I2C Buss on RP2040
    i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))

    apds9900=APDS9900LITE(i2c)      # Enable sensor
    apds9900.prox.enableSensor()    # Enable Proximit sensing

    while True:
            sleep_ms(25) # wait for readout to be ready
            print(apds9900.prox.proximityLevel)   #Print the proximity value



Hardware Set-up
---------------

Connect Vin to 3.3 V or 5 V power source, GND to ground, SCL and SDA to the appropriate pins to the Raspberry PI Pico

========== ====== ============ ======== ==============
APDS9960   Name   Remarks      RPI PICO  Function  
========== ====== ============ ======== ==============
1           VIN    +3.3V Power  36       3V3 
2           GND    Ground       GND      GND           
3           SCL    I2C clock    22       GP17 (SCL)   
4           SDA    I2C Data     21       GP16 (SDA)   
5           INT    Interrupt    26       GP20    
========== ====== ============ ======== ==============

.. raw:: html

    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images//PicoHookup.PNG">

Basics
------

Of course, you must import the device and library :)

.. code:: python

  import machine
  from time import sleep_ms
  from uPy_APDS9960.apds9960LITE import APDS9960LITE
 

To set-up the device to gather data, initialize the I2C-device using SCL and SDA pins. 
Then initialize the library.  

.. code:: python
  
  i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))
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


Debug
-----
If things does not work try to run the script below to verify that it i2c communication with the apds9960 is working as expected

.. code:: python

    import machine
    i2c =  machine.I2C(0,scl=machine.Pin(17), sda=machine.Pin(16))

    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
      print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))

      for device in devices:
        print("Decimal address: ",device," | Hexa address: ",hex(device))

        if(device==0x39): # APDS9960 Address = 0x39
            deviceID=i2c.readfrom_mem(devices[0],0x92, 1) #Get deviceID
            deviceID=int.from_bytes(deviceID,'big')       #Conv byte to int
            if(deviceID==0x29):
               deviceID=9900
            elif(deviceID==0x20):
                deviceID=9901
            else:
                deviceID=9960

            print("Found ADPS-",deviceID)

If successful the output should be:

.. code-block:: shell

  Scan i2c bus...
  i2c devices found: 1
  Decimal address:  57  | Hexa address:  0x39  
  Found ADPS- 9960


.. note:: Be aware if the output shows: ::

   "many i2c devices was listed"  check if the i2c pins are allocated correctly
   "No i2c device"                check if the power is correctly connected
  
The Device id can be 0xa8, 0xab 0x9c or 0x55.)

Sphinx documentation
====================

`Sphinx the Python Documentation Generator <http://www.sphinx-doc.org/>`_ is used for this documentation, if you like to build a local copy of the documentation install Sphinx :

.. code-block:: shell

    python -m pip install sphinx

Ceate html doc by

.. code-block:: shell

    cd docs
    make html

The html pages would be located at : docs/_build/html 

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_APDS9960/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.


