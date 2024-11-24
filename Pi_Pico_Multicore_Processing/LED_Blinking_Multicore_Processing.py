from machine import Pin
import time
import _thread

#GPIO Pin assinments for the LEDs
LED1_PIN = 14 
LED2_PIN = 15

#Initialize the LEDs as output pins
led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)

#Core 0: Task: Blink LED1 every 0.5 seconds
def core0_task():
    while True:
        led1.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
        
#Core 1 Task: Blink LED2 every 1 seconds
def core1_task():
    while True:
        led1.value(1)
        time.sleep(1.0)
        led1.value(0)
        time.sleep(1.0)
        
# Start the second core (Core 1) to run core1_task
_thread.start_new_thread(core1_task, ())

#Run core0_task on the main core (Core 0)
core0_task()