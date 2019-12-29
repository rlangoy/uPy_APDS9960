Introduction 
============

.. image:: https://readthedocs.org/projects/upy-apds9960/badge/?version=latest
    :target: https://upy-apds9960.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. raw:: html

    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images/breakoutboard.jpg" height="100px">
    
| This a APDS9960/GY-9960LLC micropython library for proximity detection. 
| Tested on ESP8266EX / ESP12-E ( NodeMCU DEVKIT 1.0) 

Work derived from 
       `python-apds9960 <https://github.com/liske/python-apds9960>`_

Installation and Dependencies
=============================
This driver depends on:

* `MicroPython <http://micropython.org/>`_

Tested on:
      | Sensor:   `GY-9960LLC <https://www.aliexpress.com/item/32738206621.html>`_
      | Devboard: Node MCU v1.0
      | Firmware: `esp8266-20191220-v1.12.bi <http://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin>`_        

Usage Example
=============

.. code-block:: python

  import machine
  from time import sleep_ms
  from uPy_APDS9960.APDS9960 import APDS9960

  #Init I2C Buss
  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

  proxSensor=APDS9960(i2c)              # Enable sensor
  proxSensor.enableProximitySensor()    # Enable Proximit sensing

  while True:
          sleep_ms(25) # wait for readout to be ready
          print(proxSensor.readProximity)   #Print the proximity value


Hardware Set-up
---------------

Connect Vin to 3.3 V or 5 V power source, GND to ground, SCL and SDA to the appropriate pins.

.. raw:: html

    <img src="https://github.com/rlangoy/uPy_APDS9960/raw/master/docs/images/APDS9960hookup.PNG" height="300px">

Basics
------

Of course, you must import the device and library :)

.. code:: python

  import machine
  from uPy_APDS9960.APDS9960 import APDS9960
 

To set-up the device to gather data, initialize the I2C-device using SCL and SDA pins. 
Then initialize the library.  

.. code:: python

  i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
  proxSensor = APDS9960(i2c)

Doc
===

`readtherocs <https://upy-apds9960.readthedocs.io/en/latest/>`_


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_APDS9960/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.


