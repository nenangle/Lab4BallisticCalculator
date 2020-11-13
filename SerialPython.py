import serial
import time

arduino = serial.Serial('COM4', 115200, timeout=.1)

data_1, data_2, data_1_old, data_2_old = 0, 0 ,0, 0
while True:
	data1 = list(arduino.readline())
	
	if len(data1) > 4:
		data1.pop(len(data1) - 1)
		data1.pop(len(data1) - 1)
		if data1[0] == 2 and len(data1) == 3:
			data_1 = data1
			
		elif data1[0] == 3 and len(data1) == 3:
			data_2 = data1
			
		elif data1[0] == 2 and len(data1) == 5:
			chrono_data1 = int.from_bytes([data1[3], data1[4]], byteorder='big')
			fps = 1 / (chrono_data1 * 0.000001)
			print("\nchrono: ", fps, " FPS\n")
			time.sleep(1)
			
		elif data1[0] == 3 and len(data1) == 5:
			chrono_data1 = int.from_bytes([data1[3], data1[4]], byteorder='big')
			fps = 1/(chrono_data1*0.000001)
			print("\nchrono: ", fps, " FPS\n")
			time.sleep(1)

	if (data_1 != data_1_old) and data_2:#(data_2 != data_2_old):
		print("Transmitter 1: ", data_1, " Transmitter 2: ", data_2)
	data_1_old = data_1
	data_2_old = data_2
	
	
	# print(data1)
	# chrono_data = []
	#chrono_data1 = 0
	# # res = ""
	# if len(data1) > 2:
	# 	data1.pop(len(data1) - 1)
	# 	data1.pop(len(data1) - 1)
	# 	print(data1)
		# if data1:
		# 	for h in data1:
		# 		res = res + chr(h)
		# 	#time.sleep(1)
		# 	print("chrono2: ", res)
		# print(data1)

# stop_time = dt.datetime.today().timestamp()
# print(stop_time - start_time)


# if len(data1) == 7:
# 	# chrono_data[0] = int.from_bytes(data1[3])
# 	# chrono_data[1] = int.from_bytes(data1[4])
# 	# chrono_data[2] = int.from_bytes(data1[5])
# 	# chrono_data[3] = int.from_bytes(data1[6])
# 	chrono_data1 = int.from_bytes([data1[3], data1[4], data1[5], data1[6]], byteorder='big')
# 	time.sleep(1)
# 	print("chrono: ", chrono_data1)







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