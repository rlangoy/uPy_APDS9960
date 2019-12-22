
Introduction
============
| This a APDS9960/GY-9960LLC micropython library for proximity detection. 
| Tested on ESP8266  

Work derived from 
       `python-apds9960 <https://github.com/liske/python-apds9960>`_

Installation and Dependencies
=============================
This driver depends on:

* `MicroPython <http://micropython.org/>`_

Tested on:
      | GY-9960LLC - https://www.aliexpress.com/item/32738206621.html?spm=a2g0s.9042311.0.0.27424c4dhr0Uo7
      | Node MCU v2
      | MicroPython v1.11-613-g8ce69288e       

Usage Example
=============

.. code-block:: python

        import machine
        from time import sleep_ms
        from uPy_APDS9960.APDS9960 import APDS9960

        i2c =  machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
        proxSensor=APDS9960(i2c, debug=True)
        proxSensor.proximityIntLowThreshold=128  # 0 -255
        proxSensor.enableProximitySensor()
        while True:
                sleep_ms(250) # wait for readout to be ready
                print(proxSensor.readProximity)

Hardware Set-up
---------------

Connect Vin to 3.3 V or 5 V power source, GND to ground, SCL and SDA to the appropriate pins.

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


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_APDS9960/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.


