import RPi.GPIO as gpio
import time

def distance(measure='cm'):
    gpio.setmode(gpio.BOARD)
    gpio.setup(5,gpio.OUT)
    gpio.setup(3,gpio.IN)
    
    gpio.output(5,False)
    while gpio.input(3) == 0:
            nosig = time.time()
    while gpio.input(3) == 1:
            sig = time.time()
    
    t1 = sig-nosig
    if measure == 'cm':
        distance = t1 / 0.000058
    #inches
    elif measure == 'in':
        distance = t1 / 0.000148
    else:
        print('improper choice of measurment: in or cm')
        distance = None
        
    gpio.cleanup()
    return distance

print(distance('cm'))
        

