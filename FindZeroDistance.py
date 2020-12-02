import math
import Ballistics
import matplotlib.pyplot as plt
import time

def Grapher(bullet, atmosphere):
	print('here66')
	simTime = 2
	time_interval = .001
	time_graph = []
	for m in range(0, int(simTime / time_interval)):
		time_graph.append(m)
	steps = int(math.floor(simTime / time_interval))
	
	crosswind = atmosphere[0]
	windDirection = atmosphere[1]
	if windDirection < 180:
		windDirection = windDirection + 180
	
	else:
		windDirection = windDirection - 180
	velocity = bullet[3] / 3.281
	
	#           0         1      2      3       4        5            6
	# bullet[caliber, grainage, G1, velocity, range, zer0_dist, seight_height]
	#                0          1          2         3        4
	# atmosphere[crosswind, direction, elevation, windage, density]
	
	angle_corrected = False
	rads = 0
	count = 0
	start_time = time.time()
	while angle_corrected == False:
		# print('atmo', atmosphere)
		# windage_angle = atmosphere[3] / float(1000)
		
		# deg = 77.6
		
		# elevation_angle = atmosphere[2] / float(1000)
		elevation_angle = rads / float(1000)
		
		# print('rads: ', round(math.radians(deg),4), ' ang: ', deg)
		
		distance_graph = []
		elevation_graph = []
		elevation_graph2 = []
		velocity_graph = []
		windage_graph = []
		
		elevation_graph_scaled = []
		velocity_graph_scaled =[]
		distance_graph_scaled = []
		elevation_graph_scaled_no_angle = []
		
		V = velocity
		windValue = crosswind * math.cos(windDirection * 0.0174533)
	
		dist_x_initial = 0
		velocity_x_initial = V * math.cos(elevation_angle) + crosswind * (-1) * math.sin(windDirection * 0.0174533)
		dist_z_initial = 0
		velocity_z_initial =  V * math.sin(elevation_angle)
		# print('initial z velocity: ', velocity_z_initial*1.094)
		
		velocity_x_instant = velocity_x_initial
		velocity_x_instant1 = velocity_x_initial
		dist_x_instant = dist_x_initial
		bullet_mass = bullet[1] * 0.0000648
		bullet_dia = bullet[0] * 0.0254
		bullet_area = math.pow(bullet_dia, 2) * 3.14 / 4
		air_density = atmosphere[4]
	
		# x1 = 0
		# z1 = 0
		# x2 = 0
		# z2 = 0
		# t_graph = []
		# v_graph = []
		# for x in range(0, steps + 1):
		# 	t_graph.append(x)
		#
		# 	reference_cd1 = Ballistics.dragCoefficient("G1", velocity_x_instant1, 343)
		#
		# 	drag_coefficient1 = bullet_mass * reference_cd1 / bullet[2] / math.pow(bullet_dia, 2.0) * 0.0014223
		#
		# 	currentTime = x * float(time_interval)
		# 	velocity_x_instant_updated1 = velocity_x_instant1 + time_interval * (
		# 			-0.5 * air_density * drag_coefficient1 * bullet_area * pow(velocity_x_instant1, 2) / bullet_mass)
		# 	velocity_x_instant1 = velocity_x_instant_updated1
		# 	# print(x, ' : ', (velocity_x_instant_updated1 * 3.281))
		# 	v_graph.append(velocity_x_instant_updated1*3.281)
	
		# plt.rcParams["figure.figsize"] = [14, 8]
		# fig2= plt.figure(2)
		# ax = fig2.add_subplot(111)
		#
		# plt.plot(t_graph, v_graph, label='bullet')
		# plt.legend()
		# plt.axhline(c='red')
		# plt.show()
		#
	
		for t in range(0, steps + 1):
	
			reference_cd = Ballistics.dragCoefficient("G1", velocity_x_instant, 343)
	
			drag_coefficient = bullet_mass * reference_cd / bullet[2] / math.pow(bullet_dia, 2.0) * 0.0014223
	
			currentTime = t * float(time_interval)
			velocity_x_instant_updated = velocity_x_instant + time_interval * (-0.5 * air_density * drag_coefficient * bullet_area * pow(velocity_x_instant, 2) / bullet_mass)
			
			dist_x_instant_updated = dist_x_instant + time_interval * (velocity_x_instant)
	
			# dist_y_instant = dist_x_instant * windage_angle
			wind_deflection = (-1) * windValue * (t * time_interval - dist_x_instant / V)
			# total_deflection = dist__instant - wind_deflection
	
			velocity_x_instant = velocity_x_instant_updated
	
			dist_x_instant = dist_x_instant_updated
			
			# z_angle = math.atan2((z2-z1)/(x2-x1))
			# velocity_z_dynamic = velocity_x_instant * math.sin(z_angle/1000)
			# dist_z_instant_dynamic = -4.905 * pow(currentTime, 2) + velocity_z_initial * currentTime + dist_z_initial - (dist_x_instant_updated * ((bullet[6] / 39.3701) / 100))
	
	
			dist_z_instant= -4.905 * pow(currentTime, 2) + velocity_z_initial * currentTime + dist_z_initial - (dist_x_instant_updated*((bullet[6]/39.3701)/100))
			dist_z_instant_orig = -4.905 * pow(currentTime, 2) + velocity_z_initial * currentTime + dist_z_initial
			dist_z_instant_no_angle= -4.905 * pow(currentTime, 2) + dist_z_initial - (dist_x_instant_updated*((bullet[6]/39.3701)/100))
			
			distance_graph.append(dist_x_instant_updated)
			elevation_graph.append(dist_z_instant)
			elevation_graph2.append(dist_z_instant_orig)
			velocity_graph.append(velocity_x_instant_updated)
			# windage_graph.append(total_deflection)
			
			elevation_graph_scaled.append(dist_z_instant*39.3701)
			elevation_graph_scaled_no_angle.append(dist_z_instant_no_angle * 39.3701)
			velocity_graph_scaled.append(velocity_x_instant_updated*3.281)
			distance_graph_scaled.append(dist_x_instant_updated*1.094)
	
		index = 0
		count = 0
		for item in distance_graph:
			if math.fabs(item - (bullet[4]/1.094)) < 1.0:
				index = count
			else:
				count += 1
		print(index, ':', distance_graph_scaled[index], ':', elevation_graph_scaled_no_angle[index])
		
		if abs(elevation_graph_scaled[index]-1.5) > 0.01:
			rads = rads + 0.005
			angle_corrected =  False
			count = count + 1
			print('Reference: ', abs(elevation_graph_scaled[index]-1.5))
		
		else:
			print('RADS:::', rads)
			angle_corrected = True
			print('Total Execution Time:', time.time() - start_time)
	# return rads
	
	# plt.rcParams["figure.figsize"] = [14, 8]

	# fig = plt.figure(1)
	# ax2 = fig.add_subplot(111)
	# ax2.plot(distance_graph_scaled, velocity_graph_scaled, label='Velocity', c='green')
	# plt.ylim([0, 3000])
	# plt.xlim([0, 1000])
	

	# fig2 = plt.figure(2)
	# ax = fig2.add_subplot(111)
	# ax.axhline(c='red')
	# plt.axvline(x=100, c='green')
	# plt.plot([0, 1500], [bullet[6], bullet[6]], color='k', linestyle='-', linewidth=2)
	# ax.set_xlabel('distance')
	# ax.set_ylabel('Elevation', color='black')
	# ax.plot(distance_graph_scaled, elevation_graph_scaled, label='Elevation', c='blue')
	# ax.plot(distance_graph_scaled, elevation_graph_scaled_no_angle, label='Elevation', c='purple')
	# plt.ylim([-5, 2.2])
	# plt.xlim([0, 200])
	# plt.show()
	#
	#
	# # plt.plot(t_graph, v_graph, label='v graph')
	#
	#
	# #           0         1      2      3       4        5            6
	# # bullet[caliber, grainage, G1, velocity, range, zer0_dist, seight_height]
	# # droop = FindElevationAngle(elevation_graph, distance_graph, bullet[5])#(float(bullet[5])/1.047) or bullet[5]
	# droop = calculation((bullet[4]/1.094), elevation_graph2, distance_graph, bullet[5], bullet[6])
	# print('droop ', droop)
	# # inches_to_moa = (abs(droop)*1.047) * (100/bullet[5]) #(float(bullet[5])*1.047) or (float(bullet[5])/1.047)
	# inches_to_moa = (abs(droop)*1.044) * (100/bullet[5]) #(float(bullet[5])*1.047) or (float(bullet[5])/1.047) (abs(droop)*1.044)
	#
	# print('moa: ', inches_to_moa)
	# moa_to_mils = (inches_to_moa / 3.4395) #3.438
	# print('mils: ', moa_to_mils)
	# return moa_to_mils


# def calculation(distance ,elevation_graph, distance_graph, sight_dist, sight_height):
# 	stop = False
# 	while stop != True:
# 		print("Made it here: 2")
# 		index = 0
# 		count = 0
# 		for item in distance_graph:
# 			if math.fabs(round(item) - round(distance)) < 1.0:
# 				index = count
# 			else:
# 				count += 1
#
# 		bullet_drop = (elevation_graph[index])* 39.3701
# 		closest_dist = distance_graph[index] * 1.094
# 		print("Bullet drop: ", bullet_drop , ' index: ', index, ' distance', distance_graph[index] * 1.094)
# 		stop = True
# 		sight_drop = closest_dist * ((sight_height) / 100)
# 		print('sight drop: ', sight_drop)
# 		overall_drop = abs(bullet_drop) + sight_drop
# 		print('Overall drop: ', overall_drop)
# 		return overall_drop
#
# def FindElevationAngle(e_graph, d_graph, z_dist):
# 	dis_vel_dict = {}
# 	for z in range(0, (len(e_graph)-1)):
# 		dis_vel_dict[z] = [round(d_graph[z] *1.0936, 4), round(39.3701 * e_graph[z], 4)] #[round(d_graph[z] * 1.0936, 3), round(39.3701 * e_graph[z], 3)]
# 		# print(dis_vel_dict[z])
# 		# print(z, ': ', (1.0936 * d_graph[z]), 'orig', (z_dist[z] * 39.3701))
#
# 	# print(dis_vel_dict)
# 	sep = 0
# 	rang = 0
# 	closest = 20.0
# 	drop = 0.0
# 	for i in range(0, (len(dis_vel_dict)-1)):
# 		sep = abs(z_dist - dis_vel_dict[i][0])
# 		if (sep < closest):
# 			closest = sep
# 			rang = dis_vel_dict[i][0]
# 			drop = dis_vel_dict[i][1]
#
# 	print("Dist: ", rang, " Drop: ", drop)
# 	return drop
	
# bullet[caliber, grainage, G1, velocity, range]
# atmosphere[crosswind, direction, elevation, windage, density]
# bullet = [float(cal), int(grain), float(coef), int(speed), int(dist), sight in, sight height]
#
# zero_distance = 100
# bullet = [0.308, 195, 0.584, 2930, 100, 100, 1.5]
# atmosphere = [0, 0, 0, 0, 1.183]

# elevation = 1.93
# inches_to_moa = 1.93/((bullet[4])/100)
# moa_to_mils = (inches_to_moa/3.438)

# el_graph, di_graph = Grapher(bullet, atmosphere)
#Grapher(bullet, atmosphere)



# print("Bullet: ",float(bullet[5]*1.0936))
# 	droop = FindElevationAngle(elevation_graph, distance_graph, bullet[5])#(float(bullet[5])/1.047) or bullet[5]
# 	print()
# 	inches_to_moa = abs(droop) / ((float(bullet[5])/1.047) / 100) #(float(bullet[5])*1.047) or (float(bullet[5])/1.047)
# 	print('moa: ', inches_to_moa)
# 	moa_to_mils = (inches_to_moa / 3.438)
# 	print('mils: ', moa_to_mils)
# 	return moa_to_mils














