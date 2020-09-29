import time
import random

def windspeed():
    for x in range(0, 1000):
        wind = random.randint(15,25)
        wind_str = str(wind)
        time.sleep(.1)
        return wind_str

def winddir():
    for x in range(0, 1000):
        wind_d = 0 #from right
        # wind_d = random.randint(40, 50)
        wind_di = str(wind_d)
        time.sleep(.1)
        return wind_di

def temp():
    for x in range(0, 1000):
        temper = random.randint(60, 62)
        temp_str = str(temper)
        time.sleep(.1)
        return temp_str

def hum():
    for x in range(0, 1000):
        humi = random.randint(50, 53)
        humi_str = str(humi)
        time.sleep(.1)
        return humi_str

def pres():
    for x in range(0, 1000):
        press = random.randint(29, 30)
        press_str = str(press)
        time.sleep(.1)
        return press_str

