import serial

arduino = serial.Serial('COM5', 115200, timeout=.1)

data_1 = 0
data_2 = 0
data_1_old = 0
data_2_old = 0
while True:

	data = list(arduino.readline())
	data1 = data
	
	if len(data) > 1:
		if data[0] == 2:
			data.pop(len(data) - 1)
			data.pop(len(data) - 1)
			data_1 = data
		elif data[0] == 3:
			data.pop(len(data) - 1)
			data.pop(len(data) - 1)
			data_2 = data

	if (data_1 != data_1_old) and data_2:
		print("Transmitter 1: ", data_1, " Transmitter 2: ", data_2)
	data_1_old = data_1
	data_2_old = data_2
	
	
	# print(data)
	# if len(data1) > 2:
	# 	data1.pop(len(data1) - 1)
	# 	data1.pop(len(data1) - 1)
	# 	print(data1)

# stop_time = dt.datetime.today().timestamp()
# print(stop_time - start_time)









# print("Lasttime: ", dt.datetime.today().timestamp())
# print("Diff: ", start_actual - start_time)
# print("Diff2: ", dt.datetime.today().timestamp() - start_time)
# print("count: ", counter)


# data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
# data1 = arduino.read()
# if data and data1:
#     if "\\x" in data:
#         data.replace("\\x", '')
#         print(data, " fixed")
#
#     else:
#         data1 = RemoveExcessChars(str(data))
#         data2 = data.decode('ascii')
#         print(" Data Original: ", data, "Data: ", data2, " Data1: ", data1)
#         #print(ord(split(data1)[0]))

# with serial.Serial('COM3', 19200, timeout=1) as ser:
#
#      x = ser.read()          # read one byte
#      s = ser.read(10)        # read up to ten bytes (timeout)
#      line = ser.readline()   # read a '\n' terminated line


# def RemoveExcessChars(message_str):
# 	rep_str = ''
# 	if message_str[0] == 'b':
# 		rep_str = message_str.replace('b', '')
#
# 	if "'" in rep_str:
# 		rep_str = rep_str.replace("'", '')
#
# 	return rep_str
#
#
# def split(word):
# 	return [char for char in word]