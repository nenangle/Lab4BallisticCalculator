from tkinter import *
import time
import math
import SimulatedConditions
import Ballistics
import FindZeroDistance
import FindZeroDistanceTest
import serial


# ---------------------------------------------------------------------------------------------------------------

def raise_frame(frame):
	frame.tkraise()


# ---------------------------------------------------------------------------------------------------------------

def AddWindDir(current_wind):
	new_windD = current_wind + 1
	return new_windD


def SubWindDir(current_wind):
	new_windD = current_wind - 1
	return new_windD

#           0         1      2      3       4        5            6
	# bullet[caliber, grainage, G1, velocity, range, zer0_dist, seight_height]
	# atmosphere[crosswind, direction, elevation, windage, density]
def Frame2Attributes(f2, cal, grn, coef, speed, dist, sight_height, zero_dist, targ_size):
	raise_frame(f2)
	cal_text = "Your Caliber: " + str(cal)
	dia_text = "Your Grainage: " + str(grn)
	coef_text = "Your Coefficient: " + str(coef)
	dist_text = "Muzzle Velocity (FPS): " + str(speed)
	range_text = "Target Range (yards): " + str(dist)
	
	bullet = [float(cal), int(grn), float(coef), int(speed), int(dist), float(zero_dist), float(sight_height)]
	
	Label(f2, text=cal_text).grid(column=1, row=1, sticky= W + E)
	Label(f2, text=dia_text).grid(column=1, row=2, sticky= W + E)
	Label(f2, text=coef_text).grid(column=1, row=3, sticky= W + E)
	Label(f2, text=dist_text).grid(column=2, row=1, sticky= W + E)
	Label(f2, text=range_text).grid(column=2, row=2, sticky= W + E)
	
	Button(f2, text='Start Logging', command=lambda: Frame2DynamicAttributes(speed, dist,
	                                bullet, int(targ_size))).grid(column=1,row=4, sticky= W + E)
	
	Button(f2, text='Go Back', command=lambda: raise_frame(f1)).grid(column=2,row=4, sticky= W + E)
	
#Frame2DynamicAttributes with serial
# ---------------------------------------------------------------------------------------------------------------

def Frame2DynamicAttributes(bullet_speed, target_range, bullet, targ_size):
	if targ_size == 1:
		scale_factor = 4
		varr = 25
		scaler = 30

	elif targ_size == 2:
		scale_factor = 2
		varr = 15
		scaler = 10

	else:
		scale_factor = 1
		varr = 10
		scaler = 10

	feet = targ_size
	inches = feet * 12

	size = 10 * 12 * feet * scale_factor
	canvas_w = size
	canvas_h = size

	x = (size / 2) - 5
	x1 = (size / 2) + 5
	y = (size / 2) - 5
	y1 = (size / 2) + 5

	simlist = SimulatedConditions.LoadData()
	first_iteration = True
	iframe1 = Frame(f2, relief=RAISED, bd=2)
	iframe1.grid(column=10, row=13)
	c = Canvas(iframe1, bg='white', width=canvas_w, height=canvas_h)

	c.grid(column=10, row=12)

	c.create_line((size / 2), 0, (size / 2), size)
	c.create_line(0, (size / 2), size, (size / 2))

	# create a hash mark every inch on x-y
	steps = 10 * scale_factor
	sizer = 5 * scale_factor
	for k in range(0, canvas_w, steps):
		c.create_line(((size / 2) - sizer), k, ((size / 2) + sizer), k)  # y hash
		c.create_line(k, ((size / 2) - sizer), k, ((size / 2) + sizer))  # x hash

	hash_counter = 1
	for f in range(10, int(canvas_w / 2), steps):
		# x hash measurement
		c.create_text(((size / 2) - f - scaler), ((size / 2) + varr), text=str(hash_counter), font=("Arial", 5))
		c.create_text(((size / 2) + f + scaler), ((size / 2) + varr), text=str(hash_counter), font=("Arial", 5))

		# y hash measurement
		c.create_text(((size / 2) + varr), ((size / 2) - f - scaler), text=str(hash_counter), font=("Arial", 5))
		c.create_text(((size / 2) + varr), ((size / 2) + f + scaler), text=str(hash_counter), font=("Arial", 5))

		hash_counter += 1

	c.create_text(((size / 2) - 20), 10, text="0")
	c.create_text(((size) - 10), ((size / 2) - 20), text="90")
	c.create_text(((size / 2) - 20), ((size) - 10), text="180")
	c.create_text(10, ((size / 2) - 20), text="270")

	mover = c.create_oval(x, y, x1, y1, fill="red")  # where bullet will land if aim is directly at center
	# inverse_mover = c.create_oval(x, y, x1, y1, fill="blue")  # where to aim

	# aids visual tracking, dynamically moving line
	mover_line_x = c.create_line((size / 2), ((size / 2) - 7), (size / 2), ((size / 2) + 7), fill="red", width = 3)
	mover_line_y = c.create_line(((size / 2) - 7), (size / 2), ((size / 2) + 7), (size / 2), fill="red", width = 3)
	# inv_mover_line_x = c.create_line((size / 2), ((size / 2) - 7), (size / 2), ((size / 2) + 7), fill="blue")
	# inv_mover_line_y = c.create_line(((size / 2) - 7), (size / 2), ((size / 2) + 7), (size / 2), fill="blue")

	ball_pos = [0, 0]
	count = 0
	done = False
	pressure = 0
	windspeed = 0
	winddir = 0
	air_density = 0
	temp = 0
	# elevation = 0.9816
	# elevation = 0.9625
	elevation = 0
	spec_gas_cont = 287.058
	arduino = serial.Serial('COM4', 115200, timeout=.1)
	done = False
	start_flag = True
	updated_bullet_speeds = []
	shot_count = 0
	check = False
	data = []
	while len(data) < 8 or check == False:
		data = list(arduino.readline())
		print('data', data)
		if len(data) > 8:
			shot_count = data[9]
			check = True
			print('pre shot count: ', shot_count)

	coun = 0
	new_vel = 0
	while 1:
		# print('HERE')
		Label(f2, text="Updated Velocity ").grid(column=1, row=10)
		vel_label = Label(f2, text=round(new_vel))
		vel_label.grid(column=2, row=10)
		if done == True:
			data1 = list(arduino.readline())

		else:
			data1 = [0]

		if len(data1) >= 10 and done == True:
			done = False
			# print('HERE')
			# print('length ', len(data1))
			data1.pop(len(data1) - 1)
			data1.pop(len(data1) - 1)
			temp = (data1[3] - 155) + 273.15
			pressure = (int.from_bytes([data1[4], data1[5]], byteorder='big')) * 100
			windspeed = data1[0]
			
			if data1[1] == 255:
				data1[1] = 0
			if data1[1] == 254:
				data1[1] = 10
			
			if data1[2] == 255:
				data1[2] = 0
			if data1[2] == 254:
				data1[2] = 10
			winddir = int.from_bytes([data1[1], data1[2]], byteorder='big')
			
			if data1[4] == 255:
				data1[4] = 0
			if data1[4] == 254:
				data1[4] = 10
				
			if data1[7] == 255:
				data1[7] = 0
			if data1[7] == 254:
				data1[7] = 10

			if start_flag:
				
				
				air_density = pressure / (temp * spec_gas_cont)
				# print('bullet', bullet[4])
				
				vel_label1 = Label(f2, text='Calculating Zero', bg = 'green')
				vel_label1.grid(column=1, row=13)
				# elevation = FindZeroDistance.Grapher(bullet, [0, 0, 0, 0, air_density])
				elevation = 1.354999999999993  # 100yd 300 win
				vel_label1.destroy()
				vel_label1 = Label(f2, text='DONE', bg='green')
				vel_label1.grid(column=1, row=13)
				
			start_flag = False

			
			try:
				if data1[9] != shot_count:
					bullet_speed = int.from_bytes([data1[7], data1[8]], byteorder='big')
					# print('Bullet Speed: ', bullet_speed)
					fps = 1 / (int(bullet_speed) * 0.000001)
					if fps < 4000:
						print('FPS: ', fps)
						updated_bullet_speeds.append(fps)
						coun = 0
						for sped in updated_bullet_speeds:
							coun = coun + sped
							print('Count::: ', coun)
		
						vel_label.destroy()
						new_vel = coun / len(updated_bullet_speeds)
						time.sleep(1)
		
						print('Shot Count: ', shot_count)
					shot_count = data1[9]
			except IndexError:
				continue

			# temp = (data1[3] - 155) + 273.15
			# pressure = (int.from_bytes([data1[4], data1[5]], byteorder='big')) * 100
			# air_density = pressure / (temp * spec_gas_cont)
		# print('Wind Speed:', data1[0], 'Wind Dir: ', winddir, 'Density:', air_density)
		
			# if wind_d == 1:
			# 	wind_d = 0
			# if bullet_speed == 1:
			# 	bullet_speed = 0
		
		# start_flag = False


		Label(f2, text="Wind speed is currently (MPH): ").grid(column=1, row=6, sticky= W + E)
		Label(f2, text=windspeed).grid(column=2, row=6, sticky= W + E)

		atmosphere = [windspeed, winddir, elevation, 0, air_density]

		Label(f2, text="Wind direction is currently (deg): ").grid(column=1, row=7, sticky= W + E)
		Label(f2, text=winddir).grid(column=2, row=7, sticky= W + E)


		move_x = BulletPhysicsWind(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere, f2, feet, scale_factor)
		move_y = BulletPhysicsGravity(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere, f2, feet, scale_factor)

		Label(f2, text="Horizontal deflection (in): ").grid(column=1, row=8, sticky= W + E)
		Label(f2, text=str(round(move_x[0], 2))).grid(column=2, row=8, sticky= W + E)

		Label(f2, text="Vertical deflection (in): ").grid(column=1, row=9, sticky= W + E)
		Label(f2, text=str(round(move_y[0], 2))).grid(column=2, row=9, sticky= W + E)

		Label(f2, text="Velocity @ Target (ft/sec): ").grid(column=1, row=11, sticky= W + E)
		Label(f2, text=str(round(move_y[2], 2))).grid(column=2, row=11, sticky= W + E)

		energy = 0.5*((bullet[1]*0.000142857)/32.185)*(move_y[2]**2)

		Label(f2, text="Energy @ Target (ft*lbs): ").grid(column=1, row=12, sticky=W + E)
		Label(f2, text=str(round(energy, 2))).grid(column=2, row=12, sticky=W + E)



		c.move(mover, move_x[1], move_y[1])  # , ball_pos)
		# c.move(inverse_mover, -move_x[1], -move_y[1])  # , ball_pos)

		c.move(mover_line_x, move_x[1], 0)
		c.move(mover_line_y, 0, move_y[1])

		# c.move(inv_mover_line_x, -move_x[1], 0)
		# c.move(inv_mover_line_y, 0, -move_y[1])

		ball_pos = BallCenter(c.coords(mover))
		# print("Cords are: ", ball_pos)
		first_iteration = False
		time.sleep(.01)
		root.update()
		count += 1
		done = True




# def Frame2DynamicAttributes(bullet_speed, target_range, bullet, targ_size):
# 	if targ_size == 1:
# 		scale_factor = 4
# 		varr = 25
# 		scaler = 30
#
# 	elif targ_size == 2:
# 		scale_factor = 2
# 		varr = 15
# 		scaler = 10
#
# 	else:
# 		scale_factor = 1
# 		varr = 10
# 		scaler = 10
#
# 	feet = targ_size
# 	inches = feet * 12
#
# 	size = 10 * 12 * feet * scale_factor
# 	canvas_w = size
# 	canvas_h = size
#
# 	# x = (size / 2) - 2.5
# 	# x1 = (size / 2) + 2.5
# 	# y = (size / 2) - 2.5
# 	# y1 = (size / 2) + 2.5
# 	x = (size / 2) - 5
# 	x1 = (size / 2) + 5
# 	y = (size / 2) - 5
# 	y1 = (size / 2) + 5
#
# 	simlist = SimulatedConditions.LoadData()
# 	first_iteration = True
# 	iframe1 = Frame(f2, relief=RAISED, bd=2)
# 	iframe1.grid(column=10, row=13)
# 	c = Canvas(iframe1, bg='white', width=canvas_w, height=canvas_h)
#
# 	c.grid(column=10, row=12)
#
# 	c.create_line((size / 2), 0, (size / 2), size)
# 	c.create_line(0, (size / 2), size, (size / 2))
#
# 	# create a hash mark every inch on x-y
# 	steps = 10 * scale_factor
# 	sizer = 5 * scale_factor
# 	for k in range(0, canvas_w, steps):
# 		c.create_line(((size / 2) - sizer), k, ((size / 2) + sizer), k)  # y hash
# 		c.create_line(k, ((size / 2) - sizer), k, ((size / 2) + sizer))  # x hash
#
# 	hash_counter = 1
# 	for f in range(10, int(canvas_w / 2), steps):
# 		# x hash measurement
# 		c.create_text(((size / 2) - f - scaler), ((size / 2) + varr), text=str(hash_counter), font=("Arial", 5))
# 		c.create_text(((size / 2) + f + scaler), ((size / 2) + varr), text=str(hash_counter), font=("Arial", 5))
#
# 		# y hash measurement
# 		c.create_text(((size / 2) + varr), ((size / 2) - f - scaler), text=str(hash_counter), font=("Arial", 5))
# 		c.create_text(((size / 2) + varr), ((size / 2) + f + scaler), text=str(hash_counter), font=("Arial", 5))
#
# 		hash_counter += 1
#
# 	c.create_text(((size / 2) - 20), 10, text="0")
# 	c.create_text(((size) - 10), ((size / 2) - 20), text="90")
# 	c.create_text(((size / 2) - 20), ((size) - 10), text="180")
# 	c.create_text(10, ((size / 2) - 20), text="270")
#
# 	mover = c.create_oval(x, y, x1, y1, fill="red")  # where bullet will land if aim is directly at center
# 	# inverse_mover = c.create_oval(x, y, x1, y1, fill="blue")  # where to aim
#
# 	# aids visual tracking, dynamically moving line
# 	mover_line_x = c.create_line((size / 2), ((size / 2) - 7), (size / 2), ((size / 2) + 7), fill="red", width = 3)
# 	mover_line_y = c.create_line(((size / 2) - 7), (size / 2), ((size / 2) + 7), (size / 2), fill="red", width = 3)
# 	inv_mover_line_x = c.create_line((size / 2), ((size / 2) - 7), (size / 2), ((size / 2) + 7), fill="blue")
# 	inv_mover_line_y = c.create_line(((size / 2) - 7), (size / 2), ((size / 2) + 7), (size / 2), fill="blue")
#
# 	ball_pos = [0, 0]
# 	count = 0
# 	current_dir = 45
# 	density = 1.183
# 	start_flag = True
# 	# elevation = 0.9816
# 	# elevation = 0.9625
# 	elevation = 0
# 	# Label(f2, text="Atmospheric Conditions").grid(column=2, row=5, sticky=W + E)
# 	while 1:
# 		windspeed = 15
# 		winddir = 0
# 		if start_flag:
# 			# elevation = FindZeroDistance.Grapher(bullet, [0, 0, 0, 0, density])
# 			# elevation = FindZeroDistanceTest.Grapher(bullet, [windspeed, winddir, 0, 0, density], elevation1)
#
# 			# elevation = FindZeroDistanceTest.Grapher(bullet, [windspeed, winddir, 0, 0, density], 0)
# 			elevation = 1.354999999999993 #100yd 300 win
# 			# elevation = 0
# 			# elevation = 1.739999999999985 #200yd 300 win
# 			# elevation = 1.359999999999993
#
# 		start_flag = False
#
# 		Label(f2, text="Wind speed is currently (MPH): ").grid(column=1, row=6, sticky= W + E)
# 		Label(f2, text=windspeed).grid(column=2, row=6, sticky= W + E)
#
# 		atmosphere = [windspeed, winddir, elevation, 0, density]
#
# 		Label(f2, text="Wind direction is currently (deg): ").grid(column=1, row=7, sticky= W + E)
# 		Label(f2, text=winddir).grid(column=2, row=7, sticky= W + E)
#
#
# 		move_x = BulletPhysicsWind(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere, f2, feet, scale_factor)
# 		move_y = BulletPhysicsGravity(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere, f2, feet, scale_factor)
#
# 		Label(f2, text="Horizontal deflection (in): ").grid(column=1, row=8, sticky= W + E)
# 		Label(f2, text=str(round(move_x[0], 2))).grid(column=2, row=8, sticky= W + E)
#
# 		Label(f2, text="Vertical deflection (in): ").grid(column=1, row=9, sticky= W + E)
# 		Label(f2, text=str(round(move_y[0], 2))).grid(column=2, row=9, sticky= W + E)
#
# 		Label(f2, text="Velocity @ Target (ft/sec): ").grid(column=1, row=10, sticky= W + E)
# 		Label(f2, text=str(round(move_y[2], 2))).grid(column=2, row=10, sticky= W + E)
#
# 		energy = 0.5*((bullet[1]*0.000142857)/32.185)*(move_y[2]**2)
#
# 		Label(f2, text="Energy @ Target (ft*lbs): ").grid(column=1, row=11, sticky=W + E)
# 		Label(f2, text=str(round(energy, 2))).grid(column=2, row=11, sticky=W + E)
#
#
#
# 		c.move(mover, move_x[1], move_y[1])  # , ball_pos)
# 		# c.move(inverse_mover, -move_x[1], -move_y[1])  # , ball_pos)
#
# 		c.move(mover_line_x, move_x[1], 0)
# 		c.move(mover_line_y, 0, move_y[1])
#
# 		# c.move(inv_mover_line_x, -move_x[1], 0)
# 		# c.move(inv_mover_line_y, 0, -move_y[1])
#
# 		ball_pos = BallCenter(c.coords(mover))
# 		# print("Cords are: ", ball_pos)
# 		first_iteration = False
# 		time.sleep(.01)
# 		root.update()
# 		count += 1


# ---------------------------------------------------------------------------------------------------------------
def BallCenter(coor):
	x = (coor[0] + coor[2]) / 2
	y = (coor[1] + coor[3]) / 2
	cord = [x, y]
	return cord

# ---------------------------------------------------------------------------------------------------------------
#size, int(target_range), first_iteration, ball_pos, bullet, atmosphere, f2,feet, scale_factor)
def BulletPhysicsWind(size, range1, iteration, position, bullet, atmosphere, f2, feet, scale):  # atmosphere[crosswind, direction, elevation, windage, density]
	target_size = (size / scale) / 10

	drop, deflection, speed = Ballistics.trajectoryGraph(bullet, atmosphere)  # -(wind_vect * (((test_time) - (range1 / speed)))) #deflection goes in the opposite direction of the wind direction
	# print('Def: ', deflection)
	x_movement = [0, 0]
	deflection = (-1) * deflection
	x_movement[0] = (deflection)
	
	def_2_pix = (deflection / target_size) * size
	int_def_2_pix = int(round(def_2_pix,1))
	
	position_vector_old = position[0] - (size / 2)  # old position distance from y-axis
	position_vector_new = (int_def_2_pix + (size / 2)) - (size / 2)  # if (+) right side of y-ax; if (-) left side of y-ax
	
	if (iteration):  # if it is the first iteration return the full deflection
		x_movement[1] = def_2_pix
		return x_movement
	
	elif (iteration == False and position_vector_old < position_vector_new):  # if it isnt the first iter & the deflection than before is more calculate new deflection and add the difference
		def_diff = abs(position_vector_new - position_vector_old)  # ex) old = -7; new = -5; dist = 2; move 2 right
		# need to add diffence in deflection to account for drift
		x_movement[1] = def_diff
		return x_movement
	
	
	elif (iteration == False and position_vector_old > position_vector_new):  # if it isnt the first iter & the deflection is less than before calculate new deflection and sub the difference
		def_diff = abs(position_vector_old - position_vector_new)  # ex) old = -5; new = -7 dist = 2; move 2 left
		# need to sub diffence in deflection to account for drift
		x_movement[1] = -def_diff
		return x_movement
	
	else:  # if it isnt the first iter & the def hasnt changed
		def_2_pix = 0  # return 0 for no change on graph
		x_movement[1] = def_2_pix
		return x_movement

# ---------------------------------------------------------------------------------------------------------------
# 39.3701 * elevation_graph[index], 39.3701 * windage_graph[index], velocity_graph[index] * 3.28084
def BulletPhysicsGravity(size, range1, iteration, position, bullet, atmosphere, f2, feet, scale):
	target_size = (size / scale) / 10

	drop, deflection, speed = Ballistics.trajectoryGraph(bullet,atmosphere)  # -(wind_vect * (((test_time) - (range1 / speed)))) #deflection goes in the opposite direction of the wind direction
	
	y_movement = [0, 0, 0]
	
	deflection = (drop - bullet[6])
	y_movement[0] = deflection
	
	def_2_pix = (deflection / target_size) * size
	int_def_2_pix = int(round(def_2_pix,1))
	
	position_vector_old = position[1] - (size / 2)  # old position distance from y-axis
	position_vector_new = (int_def_2_pix + (size / 2)) - (size / 2)  # if (+) right side of y-ax; if (-) left side of y-ax
	
	if (iteration):  # if it is the first iteration return the full deflection
		y_movement[1] = def_2_pix
		y_movement[2] = speed
		return y_movement
	
	elif (iteration == False and position_vector_old < position_vector_new):  # if it isnt the first iter & the deflection than before is more calculate new deflection and add the difference
		def_diff = abs(position_vector_new - position_vector_old)  # ex) old = -7; new = -5; dist = 2; move 2 right
		y_movement[1] = def_diff
		y_movement[2] = speed
		return y_movement
	
	elif (iteration == False and position_vector_old > position_vector_new):  # if it isnt the first iter & the deflection is less than before calculate new deflection and sub the difference
		def_diff = abs(position_vector_old - position_vector_new)  # ex) old = -5; new = -7 dist = 2; move 2 left
		y_movement[1] = -def_diff
		y_movement[2] = speed
		return y_movement
	
	else:  # if it isnt the first iter & the def hasnt changed
		def_2_pix = 0  # return 0 for no change on graph
		y_movement[1] = def_2_pix
		y_movement[2] = speed
		return y_movement


# ---------------------------------------------------------------------------------------------------------------
root = Tk()
f1 = Frame(root)
f2 = Frame(root)

for frame in (f1, f2):
	frame.grid(row=0, column=0, sticky='news')
root.title("Ballistic Calculator")
root.geometry("850x725")

cal = ['0.308', '195', '0.584', '2930', '100', '1.5', '100']

Label(f1, text='Enter Bullet Diameter (in)').grid(column=1, row=1)
cal_entry = Entry(f1, width=5)
cal_entry.insert(0, cal[0])
cal_entry.grid(column=2, row=1)

Label(f1, text='Enter Bullet Grain').grid(column=1, row=2)
bullet_entry = Entry(f1, width=5)
bullet_entry.insert(0, cal[1])
bullet_entry.grid(column=2, row=2)

Label(f1, text='Enter Ballistic Coefficient (G1)').grid(column=1, row=3)
ballistic_entry = Entry(f1, width=5)
ballistic_entry.insert(0, cal[2])
ballistic_entry.grid(column=2, row=3)

Label(f1, text='Enter Bullet Velocity (FPS)').grid(column=1, row=4)
velocity_entry = Entry(f1, width=5)
velocity_entry.insert(0, cal[3])
velocity_entry.grid(column=2, row=4)

Label(f1, text='Enter Target Distance (yards)').grid(column=1, row=5)
distance_entry = Entry(f1, width=5)
distance_entry.insert(0, cal[4])
distance_entry.grid(column=2, row=5)

Label(f1, text='Enter Sight Height (in)').grid(column=1, row=6)
sight_height_entry = Entry(f1, width=5)
sight_height_entry.insert(0, cal[5])
sight_height_entry.grid(column=2, row=6)

Label(f1, text='Enter Zero Distance (yards)').grid(column=1, row=7)
zero_dist_entry = Entry(f1, width=5)
zero_dist_entry.insert(0, cal[6])
zero_dist_entry.grid(column=2, row=7)

Label(f1, text='Enter Target Size (feet)').grid(column=1, row=8)
target_entry = Entry(f1, width=5)
target_entry.insert(0, '2')
target_entry.grid(column=2, row=8)

Label(f1, text='Press Enter When Done').grid(column=1, row=9)
Button(f1, text='Enter',
       command=lambda: Frame2Attributes(f2, cal_entry.get(), bullet_entry.get(), ballistic_entry.get(),
                                        velocity_entry.get(), distance_entry.get(), sight_height_entry.get(),
                                        zero_dist_entry.get(), target_entry.get())).grid(column=2, row=9)

raise_frame(f1)
root.mainloop()

# Label(f1, text='Enter Bullet Diameter (in)').grid(column=1, row=1)
# cal_entry = Entry(f1, width=5)
# cal_entry.insert(0, '0.308')
# cal_entry.grid(column=2, row=1)
#
# Label(f1, text='Enter Bullet Grain').grid(column=1, row=2)
# bullet_entry = Entry(f1, width=5)
# bullet_entry.insert(0, '195')
# bullet_entry.grid(column=2, row=2)
#
# Label(f1, text='Enter Ballistic Coefficient (G1)').grid(column=1, row=3)
# ballistic_entry = Entry(f1, width=5)
# ballistic_entry.insert(0, '0.584')
# ballistic_entry.grid(column=2, row=3)
#
# Label(f1, text='Enter Bullet Velocity (FPS)').grid(column=1, row=4)
# velocity_entry = Entry(f1, width=5)
# velocity_entry.insert(0, '2930')
# velocity_entry.grid(column=2, row=4)
#
# Label(f1, text='Enter Target Distance (yards)').grid(column=1, row=5)
# distance_entry = Entry(f1, width=5)
# distance_entry.insert(0, '100')
# distance_entry.grid(column=2, row=5)
#
# Label(f1, text='Enter Sight Height (in)').grid(column=1, row=6)
# sight_height_entry = Entry(f1, width=5)
# sight_height_entry.insert(0, '1.5')
# sight_height_entry.grid(column=2, row=6)
#
# Label(f1, text='Enter Zero Distance (yards)').grid(column=1, row=7)
# zero_dist_entry = Entry(f1, width=5)
# zero_dist_entry.insert(0, '100')
# zero_dist_entry.grid(column=2, row=7)