# MicroPython-INA260

MicroPython driver (in progress) for the TI INA260 current and power sensor. This library is heavily based on the original [Adafruit-CircuitPython-INA260](https://github.com/adafruit/Adafruit_CircuitPython_INA260) library, but changed and stripped down to work with MicroPython. This library should now be usable with boards like the [Pycom FiPy](https://pycom.io/product/fipy/).

## Usage Example

This code example is based on the usage of the [Pycom FiPy](https://pycom.io/product/fipy/).

```python
from ina260 import INA260
from machine import I2C

ina260 = INA260(I2C())

print("Current:", ina260.current)
print("Voltage:", ina260.voltage)
print("Power:", ina260.power)
```

## Disclaimer

This is a work in progress and a cross between Adafruit's library and chrisb2's [MicroPython INA219 library](https://github.com/chrisb2/pyb_ina219). The code has the basis for but lacks features like power save. Please send in a Pull Request when you want to refactor code or add features.
