# Source: Electrocredible.com, Language: MicroPython

from machine import Pin,I2C
from bmp280 import *
import time

sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
time.sleep(0.1)
bmp = BMP280(bus)

bmp.use_case(BMP280_CASE_INDOOR)
sea_press = 101325#this is dependent on local conditions
p_0 = bmp.pressure
t_0 = bmp.temperature + 273.15
alt_0=(pow((p_0/sea_press),(1/5.257))-1)*(t_0)/(0.0065)#this is a guess, you should use actualy numbers instead
while True:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    temperature=bmp.temperature  + 273.15
    print("Temperature: {} K".format(temperature))
    
    #outdated(innaccurate) version
    #approximate barometic pressure at sea level (Pa)
    #Note!!! this should draw from a regularly updated database or this will cause big difference
    #alt = (pow((sea_press / pressure), 0.1903) -1)*((temperature)/0.0065) - alt_0
    
    alt_diff = ((pow((pressure/p_0),(1/5.257))-1)*(temperature)/(0.0065))
    #this one assumes no change in T vs H
    print("Pressure: {} Pa, {} bar, {} mmHg".format(pressure,p_bar,p_mmHg))
    print("altitude (guess): {} m".format(alt_0 - alt_diff))
    print("altitude diff from boot: {} m".format(0-alt_diff))
    time.sleep(.5)