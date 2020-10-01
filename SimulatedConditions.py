import time
import random
import xlrd

def LoadData():
    exc = r"C:\Users\Nathan Nangle\Desktop\Lab 4\weather.xlsx"
    wb = xlrd.open_workbook(exc)
    sheet = wb.sheet_by_index(0)
    windlist = [0]
    for i in range(2, sheet.nrows):
        windlist.append(round(2.2 * sheet.cell_value(i, 6)))
    return windlist

def windspeed(i, data_list):
    exc = r"C:\Users\Nathan Nangle\Desktop\Lab 4\weather.xlsx"
    wb = xlrd.open_workbook(exc)
    sheet = wb.sheet_by_index(0)
    #data_list = [0]

    #wind = data_list[i]
    wind_str = str(data_list[i])
    time.sleep(.05)
    #print("Windspeed: ", wind_str, " data point: ", i)
    return wind_str

def winddir():
    for x in range(0, 1000):
        wind_d = 45 #from right
        # wind_d = random.randint(40, 50)
        wind_di = str(wind_d)
        time.sleep(.05)
        return wind_di

def temp():
    for x in range(0, 1000):
        temper = random.randint(60, 62)
        temp_str = str(temper)
        time.sleep(.05)
        return temp_str

def hum():
    for x in range(0, 1000):
        humi = random.randint(50, 53)
        humi_str = str(humi)
        time.sleep(.05)
        return humi_str

def pres():
    for x in range(0, 1000):
        press = random.randint(29, 30)
        press_str = str(press)
        time.sleep(.05)
        return press_str

