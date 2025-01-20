from machine import Pin, UART
import time

# Initialize UART0 
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

# Variable to store GPS data
gps_data = {
    "hour": "",
    "minute": "",
    "second": "",
    "latitude": "",
    "longitude": "",
    "altitude": "",
    "satellites": "",
    "date": "",
}

def parse_gps_data(nmea_sentence):
    global gps_data

    # Check for GPGGA or GPRMC sentence
    # NOTE: GPGSA and GPGSV do not give important information, but they can also be extracted if needed
    
    if nmea_sentence.startswith('$GPGGA'):
        try:
            # Split the sentence by commas
            data = nmea_sentence.split(',')
            
            # Extract relevant data from GPGGA sentence
            gps_data["hour"] = data[1][0:2]  # Hour
            gps_data["minute"] = data[1][2:4]  # Minute
            gps_data["second"] = data[1][4:6]  # Second
            gps_data["latitude"] = data[2]  # Latitude
            gps_data["longitude"] = data[4]  # Longitude
            gps_data["altitude"] = data[9]  # Altitude
            gps_data["satellites"] = data[7]  # Number of satellites

        except IndexError:
            print("Error parsing GPGGA data") 
    
    elif nmea_sentence.startswith('$GPRMC'):
        try:
            # Split the sentence by commas
            data = nmea_sentence.split(',')
            
            # Extract relevant data from GPRMC sentence
            gps_data["hour"] = data[1][0:2]  # Hour
            gps_data["minute"] = data[1][2:4]  # Minute
            gps_data["second"] = data[1][4:6]  # Second
            gps_data["latitude"] = data[3]  # Latitude
            gps_data["longitude"] = data[5]  # Longitude
            gps_data["date"] = data[9]  # Date in DDMMYY format

        except IndexError:
            print("Error parsing GPRMC data")

def format_date(date):
    # Convert date from DDMMYY to MM/DD/YY format.

    day = date[0:2]
    month = date[2:4]
    year = date[4:6]
    return f"{month}/{day}/{year}"

def read_gps():
    # Read GPS data from the UART buffer and parse it.
   
    gps_sentence = "" # empty string

    # Read data if any available
    while uart.any():
        data = uart.read(1)
        if data:
            char = data.decode('utf-8')
            gps_sentence += char

            if char == '\n' and gps_sentence: 
                parse_gps_data(gps_sentence) # Read and extract information in each NMEA sentence (once a new line is detected)
                gps_sentence = ""  # Reset for next sentence

def print_gps_data():

    if gps_data["latitude"] and gps_data["longitude"]: #print if coordinates exist
        formatted_date = format_date(gps_data["date"]) if gps_data["date"] else "N/A"
        print("Time: ", gps_data["hour"] + ":" + gps_data["minute"] + ":" + gps_data["second"]) # Time
        print("Date: ", formatted_date) # Date 
        print("Latitude: ", gps_data["latitude"])
        print("Longitude: ", gps_data["longitude"])
        print("Altitude: ", gps_data["altitude"])
        print("Satellites: ", gps_data["satellites"]) # Can be finnicky (display decimals), possibly if signal is not strong enough
        print("-" * 25) 

while True: #Loop
    read_gps()
    print_gps_data()
    time.sleep(1)  # Delay 1 sec
