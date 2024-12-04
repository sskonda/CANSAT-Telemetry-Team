#"getPressure" and "getTemp" function not implemented,
#but should return the pressure (as Pa) and temp (as *K) as floats
def getPressure():
    return 100000

def getTemp():
    return 300.0

#method 1: statistical approximation (Pa, *k) (bad)
def approxAlt(pressure, temp)
    #input pressure as Pa
    sea_press = 101325
    #approximate barometic pressure at sea level (Pa)
    #Note!!! this should draw from a regularly updated database or this will cause big difference
    return (pow((sea_press / pressure), 0.1903) -1)*(temp)/0.0065


#method 2: calibrated altitude difference measuring (Pa, m, *k)
#measure a pressure at ground level and record the altitude at ground level
#perhaps use the approximation function for an inital height?
#p0 = initial pressure, h0 = initial height
#p = most recent pressure reading, t0 = temperature at starting height
def altDifference(p0, p, h0, t0):
    return(t0/.65)*pow(1-(p/p0),19.0294)

#flow of operation:
def main():
    start_press = getPressure()
    start_temp = getTemp()
    sea_press = 101325  #Note!!! this should draw from a regularly updated database or this will cause big difference
    start_height = altDifference(sea_press, start_press, 0, start_temp)
    #...
    while(flying):
        height = start_height + altDifference(start_press, getPressure(), start_height, start_temp)
    
