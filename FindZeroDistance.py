import math
import Ballistics
import matplotlib.pyplot as plt
def Grapher(bullet, atmosphere):
	simTime = 2
	time_interval = .001
	time_graph = []
	for m in range(0, int(simTime / time_interval)):
		time_graph.append(m)
	steps = int(math.floor(simTime / time_interval))
	crosswind = atmosphere[0]
	windDirection = atmosphere[1]
	velocity = bullet[3] / 3.281
	elevation_angle = atmosphere[2] / float(1000)
	windage_angle = atmosphere[3] / float(1000)

	distance_graph = []
	elevation_graph = []
	velocity_graph = []
	windage_graph = []
	
	V = velocity
	windValue = crosswind * math.cos(windDirection * 0.0174533)

	dist_x_initial = 0
	velocity_x_initial = V * math.cos(elevation_angle) + crosswind * (-1) * math.sin(windDirection * 0.0174533)
	dist_z_initial = 0
	velocity_z_initial = V * math.sin(elevation_angle)
	
	velocity_x_instant = velocity_x_initial
	dist_x_instant = dist_x_initial
	bullet_mass = bullet[1] * 0.0000648
	bullet_dia = bullet[0] * 0.0254
	bullet_area = math.pow(bullet_dia, 2) * 3.14 / 4
	air_density = atmosphere[4]
	
	for t in range(0, steps + 1):

		reference_cd = Ballistics.dragCoefficient("G1", velocity_x_instant, 343)

		drag_coefficient = bullet_mass * reference_cd / bullet[2] / math.pow(bullet_dia, 2.0) * 0.0014223

		currentTime = t * float(time_interval)
		velocity_x_instant_updated = velocity_x_instant + time_interval * (
				-0.5 * air_density * drag_coefficient * bullet_area * pow(velocity_x_instant, 2) / bullet_mass)
		dist_x_instant_updated = dist_x_instant + time_interval * (velocity_x_instant)

		dist_y_instant = dist_x_instant * windage_angle
		wind_deflection = (-1) * windValue * (t * time_interval - dist_x_instant / V)
		total_deflection = dist_y_instant - wind_deflection

		velocity_x_instant = velocity_x_instant_updated

		dist_x_instant = dist_x_instant_updated
		print(dist_x_instant_updated, "init: ", dist_x_instant_updated*((bullet[6])/100))
		dist_z_instant = -4.905 * pow(currentTime, 2) + velocity_z_initial * currentTime + dist_z_initial #- (dist_x_instant_updated*((bullet[6]/39.3701)/100))
		
		distance_graph.append(dist_x_instant_updated)
		elevation_graph.append(dist_z_instant)
		velocity_graph.append(velocity_x_instant_updated)
		windage_graph.append(total_deflection)
		
	
	
	droop = FindElevationAngle(elevation_graph, distance_graph, bullet[5])
	inches_to_moa = abs(droop) / ((float(bullet[5])*1.047) / 100)
	moa_to_mils = (inches_to_moa / 3.438)
	return moa_to_mils

def FindElevationAngle(e_graph, d_graph, z_dist):
	dis_vel_dict = {}
	for z in range(0, (len(e_graph)-1)):
		dis_vel_dict[z] = [round(d_graph[z] * 1.0936, 3), round(39.3701 * e_graph[z], 3)]
	print(dis_vel_dict)
	sep = 0
	rang = 0
	closest = 20.0
	drop = 0.0
	for i in range(0, (len(dis_vel_dict)-1)):
		sep = abs(z_dist - dis_vel_dict[i][0])
		if (sep < closest):
			closest = sep
			rang = dis_vel_dict[i][0]
			drop = dis_vel_dict[i][1]
			
	print("Dist: ", rang, " Drop: ", drop)
	return drop
	
# bullet[caliber, grainage, G1, velocity, range]
# atmosphere[crosswind, direction, elevation, windage, density]
# bullet = [float(cal), int(grain), float(coef), int(speed), int(dist), sight in, sight height]

zero_distance = 100
bullet = [0.308, 195, 0.584, 2930, 100, 100, 1.5]
atmosphere = [0, 0, 0, 0, 1.183]

# elevation = 1.93
# inches_to_moa = 1.93/((bullet[4])/100)
# moa_to_mils = (inches_to_moa/3.438)

# el_graph, di_graph = Grapher(bullet, atmosphere)
#Grapher(bullet, atmosphere)


















