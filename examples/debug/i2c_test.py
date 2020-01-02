import machine
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))

    if(device==0x39): # APDS9960 Address = 0x39
        deviceID=i2c.readfrom_mem(devices[0],0x92, 1) #G et deviceID
        print("Found ADPS9960: Device ID: ",deviceID)