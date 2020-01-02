MicroPython APDS-9960 RAM optimized Library
===========================================

.. image:: https://readthedocs.org/projects/upy-apds9960/badge/?version=latest
    :target: https://upy-apds9960.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

|
.. raw:: html 
    
    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images/breakoutboard.jpg">

Another APDS9960 / GY-9960LLC micro python library optimized for ESP8266 / ESP12-E for:
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
      | Devboard: Node MCU v1.0
      | Firmware: `esp8266-20191220-v1.12.bi <http://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin>`_        

Installation
============
* Flash the ESP8266 with MicroPython
* Copy the folder uPy_APDS9960 and content (apds9960.py and apds9960lite.py) to the ESP8266 root folder

The steps above is descsribed in the `Thonny IDE tutorial`_.

.. _Thonny IDE tutorial: https://upy-apds9960.readthedocs.io/en/latest/thonny_guide.html



Usage Example
=============

.. code-block:: python

  import machine
  from time import sleep_ms
  from uPy_APDS9960.APDS9960LITE import APDS9960LITE

  #Init I2C Buss
  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

  apds9960=APDS9960LITE(i2c)         # Enable sensor
  apds9960.prox.enableProximity()    # Enable Proximit sensing

  while True:
          sleep_ms(25) # wait for readout to be ready
          print(apds9960.prox.readProximity)   #Print the proximity value


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
  from uPy_APDS9960.APDS9960LITE import APDS9960LITE
 

To set-up the device to gather data, initialize the I2C-device using SCL and SDA pins. 
Then initialize the library.  

.. code:: python

  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
  apds9960=APDS9960LITE(i2c)         # Enable sensor
  

Proximity
~~~~~~~~~
Proximity funxtionalites is accessed torough the apds9960.prox member class :class:`.PROX`

.. code:: python

  apds9960.prox.enableProximity()     # Enable Proximity sensing
  sleep_ms(25)                        # wait for readout to be ready
  print(apds9960.prox.readProximity)  # Print the proximity value

Light Sensing
~~~~~~~~~~~~~
Proximity funxtionalites is accessed torough the apds9960.als member class :class:`.ALS`

.. code:: python

  apds9960.als.enableLightSensor()      # Enable Light sensor
  sleep_ms(25)                          # Wait for readout to be ready
  print(apds9960.als.ambientLightLevel) # Print the ambient light value


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


