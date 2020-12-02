import time
import random
import xlrd

def LoadData():
    exc = r"C:\Users\Nathan Nangle\Desktop\Lab 4\weather.xlsx"
    wb = xlrd.open_workbook(exc)
    sheet = wb.sheet_by_index(0)
    windlist = [0]
    for i in range(2, 1000):
        windlist.append(sheet.cell_value(i, 7))
    return windlist

def windspeed():
    # wind_str = str(data_list[i])
    wind_str = float

    return wind_str

def winddir():
    #for x in range(0, 1000):
    wind_dir = (float)
        

def temp():
    for x in range(0, 1000):
        # temper = random.randint(60, 62)
        temper = 60
        temp_str = str(temper)
        time.sleep(.05)
        return temp_str

def hum():
    for x in range(0, 1000):
        # humi = random.randint(50, 53)
        humi = 50
        humi_str = str(humi)
        time.sleep(.05)
        return humi_str

def pres():
    for x in range(0, 1000):
        # press = random.randint(29, 30)
        press = 30
        press_str = str(press)
        time.sleep(.05)
        return press_str

