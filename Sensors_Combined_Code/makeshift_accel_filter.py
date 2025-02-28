import time
import board
import adafruit_bno055
import excess_d_filter

#UNCONFIGURED
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
y = [0]
v = 0
accel = (0,0,0)
acc_list = []
accel_y = [0]
filter_size = 10
filter_tolerance = 4
dt = .1 #time steo size (seconds)
for x in range(filter_size):
    accel = sensor.linear_acceleration
    acc_list.append(accel)
    accel_y.append(accel[1])#the docs don't make this clear, I'll have to check this myself      
    v += accel[1]*dt
    y += v*dt
    time.sleep(dt)
while True:
    accel = sensor.linear_acceleration
    if accel_y[-1] == "n":
        #interpolate bad data
        if excess_d_filter(accel_y[:-1], accel[1], filter_size, filter_tolerance*2) == True:
            accel_y[-1] = (accel[1] + accel_y[-2])/2   
        else:
            accel_y[-1] = accel_y[-2]
        v += accel_y[-1]*dt
    if excess_d_filter(accel_y, accel[1], filter_size, filter_tolerance) == True:
        accel_y.append(accel[1])
        v += accel[1]*dt
    else: #trend placeholder insertion
        accel_y.append("n")
    y += v*dt

        

    
        
