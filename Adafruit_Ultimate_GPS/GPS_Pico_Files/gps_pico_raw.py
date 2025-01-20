from machine import Pin, UART
import time

# Initialize UART0
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

def read_gps(): #Read GPS data from the UART buffer.

    gps_sentence = "" #initialize empty string to begin storing
    
    while uart.any(): # If any data in UART buffer
        data = uart.read(1) #Read 1 byte
        if data: # Confirm data byte exists
            char = data.decode('utf-8') #decode byte into characters
            gps_sentence += char #append to string
            
            if char == '\n' and gps_sentence: # End of sentence detected by new line
                print(gps_sentence.strip())  # Print the raw NMEA sentence
                gps_sentence = ""  # Reset string for next sentence

while True: # Infinite loop of reading NMEA sentences
    read_gps()
    time.sleep(1)  # Delay 1 second