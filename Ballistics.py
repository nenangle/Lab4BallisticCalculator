import matplotlib.pyplot as plt
from math import pow as pow
import math,random
import csv
import datetime

def trajectoryGraph(bullet, atmosphere):
    simTime = 2
    time_interval = .01
    steps = int(math.floor(simTime / time_interval))

    # bullet[caliber, grainage, G1, velocity, range]
    # atmosphere[crosswind, direction, elevation, windage, density]

    # ENVIRONMENT & BULLET PARAMETERS
    # CROSSWIND & DIRECTION DEFAULTS 0
    crosswind = atmosphere[0]
    windDirection = atmosphere[1]
    velocity = bullet[3]
    elevation_angle = atmosphere[2] / float(1000)
    windage_angle = atmosphere[3] / float(1000)
    # bullet = bullet

    # Graphing Units
    # Default units are meters, therefore initial conversion factors are 1:1
    # elevation_conversion = 1
    # distance_conversion = 1
    # elevation = 'm'
    # windage = 'm'
    # distance = 'm'

    # Initialize arrays holding graph data
    distance_graph = []
    elevation_graph = []
    velocity_graph = []
    windage_graph = []

    # Initial Conditions
    # STD Units are m/s, if imperial (fps, mph) they are converted
    # Angles converted from degrees to radians

    V = velocity
    windValue = crosswind * math.cos(windDirection * 0.0174533)

    # Initial Distance  / Velocity [v] in X, Z components
    # (-1)*sin(Crosswind) since crosswind is defined as 90degrees opposing the bullet velocity
    dist_x_initial = 0
    velocity_x_initial = V * math.cos(elevation_angle) + crosswind * (-1) * math.sin(windDirection * 0.0174533)
    dist_z_initial = 0
    velocity_z_initial = V * math.sin(elevation_angle)

    velocity_x_instant = velocity_x_initial
    dist_x_instant = dist_x_initial
    # Bullet mass in kg converted from grains
    bullet_mass = bullet[1] * 0.0000648
    # Bullet diameter from inch to meters
    bullet_dia = bullet[0] * 0.0254
    # Bullet cross area
    bullet_area = math.pow(bullet_dia, 2) * 3.14 / 4

    # Density of air
    air_density = atmosphere[4]

    for t in range(0, steps + 1):
        # Calculate BC for the velocity
        #print("vel: ", velocity_x_initial)
        reference_cd = dragCoefficient("G1", velocity_x_instant, 343)
       # print("this: ",bullet_dia, " : ", math.pow(bullet_dia, 2.0), type(reference_cd), " : ", reference_cd)
        drag_coefficient = bullet_mass * reference_cd / bullet[2] / math.pow(bullet_dia, 2.0) * 0.0014223

        # CALCULATE BULLET DROP AND VELOCITY
        currentTime = t * float(time_interval)
        velocity_x_instant_updated = velocity_x_instant + time_interval * (
                    -0.5 * air_density * drag_coefficient * bullet_area * pow(velocity_x_instant, 2) / bullet_mass)
        dist_x_instant_updated = dist_x_instant + time_interval * (velocity_x_instant)

        # Calculate Windage Effects (y direction, From right to left is positive direction)
        # Formula uses m/s for windspeed
        # Initial windage adjustment
        dist_y_instant = dist_x_instant * windage_angle
        wind_deflection = (-1) * windValue * (t * time_interval - dist_x_instant / V)
        total_deflection = dist_y_instant - wind_deflection

        # velocity_x_instant is instantaneous velocity at current distance down range (x direction)
        # dist_x_instant is current distance downrange
        # Since solved iteratively, instant is for start of the loop, updated for the end
        velocity_x_instant = velocity_x_instant_updated
        dist_x_instant = dist_x_instant_updated
        # Bullet Drop due to Gravity
        # my'' = -mg
        # y' = -gt + y'(0)

        # velocity_z_instant is instantaneous velocity in z direction at current distance downrange
        # dist_z_instant is displacement (height above reference) of bullet at current distance downrange
        velocity_z_instant = -9.81 * currentTime + velocity_z_initial
        dist_z_instant = -4.905 * pow(currentTime, 2) + velocity_z_initial * currentTime + dist_z_initial

        distance_graph.append(dist_x_instant_updated)
        elevation_graph.append(dist_z_instant)
        velocity_graph.append(velocity_x_instant_updated)
        windage_graph.append(total_deflection)

        # return_info = [0,0,0]
        # while return_info[2] != 1:
        #     print("ret: ", return_info)
        #     print("type: ", type(return_info))
        #     return_info = calculation(bullet[4], elevation_angle, windage_angle, elevation_graph, distance_graph,
        #                               windage_graph, simTime, time_interval)
        # return return_info
    returned_thing = calculation(bullet[4], elevation_angle, windage_angle, elevation_graph, distance_graph,
                    windage_graph, simTime, time_interval)
    print("adjustments string: ", returned_thing)
    return returned_thing
# ---------------------------------------------------------------------------------------------------------------------------

def calculation(distance, elevation_angle, windage_angle, elevation_graph, distance_graph, windage_graph, simTime, time_intereval):
    adjustments = {"elevation": 0, "windage": 0}
    stop = False
    previous_elevation_angle = 0
    previous_windage_angle = 0
    # If yards is used for desired distance, convert from meters
    # if unit == 'yd':
    #     distance = distance/1.09361

    while stop != True:
        index = 0
        count = 0
        for item in distance_graph:
            if math.fabs(round(item) - round(distance)) < 10.0:
                index = count
            else:
                count += 1

        bullet_drop = elevation_graph[index]
        drop_adjustment = -1 * bullet_drop / distance

        wind_deflection = windage_graph[index]
        windage_adjustment = -1 * wind_deflection / distance

        stop = True
        # if unit == 'yd':
        #distance = distance*1.09361
        # print("MIL Elevation Adjustment for " + str(distance) + "m is " + str(round(elevation_angle * 1000, 1)))
        # print("MOA Elevation Adjustment for " + str(distance) + "m is " + str(round(elevation_angle * 1000 * 3.44, 1)))
        # print("MIL Windage Adjustment for " + str(distance) + "m is " + str(round(windage_angle * 1000, 1)))
        # print("MOA Windage Adjustment for " + str(distance) + "m is " + str(round(windage_angle * 1000 * 3.44, 1)))
        adjustments1 = {}
        adjustments["elevation"] = round(elevation_angle * 1000, 1)
        adjustments["windage"] = round(windage_angle * 1000, 1)

        # print("bullet drop: ", 39.3701*elevation_graph[index])
        # print("length of elev:", len(elevation_graph))
        # print("wind_deflection: ", 39.3701*windage_graph[index])
        # print("length of wind:", len(windage_graph))
        # print(distance_graph)


        array_length = simTime / time_intereval
        adjustments1["elevation"] = 39.3701*elevation_graph[index]
        adjustments1["deflection"] = 39.3701*windage_graph[index]
        if(array_length < len(elevation_graph)):

            adjustments_arr = [39.3701*elevation_graph[index],39.3701*windage_graph[index]]

            adjustments_arr.sort()
            return adjustments_arr

        #return adjustments


# ---------------------------------------------------------------------------------------------------------------------------
# def SendWindage():
#
# def SendElevation():

def dragCoefficient(model, velocity, mach_conversion):
    if model == "G1":
        with open(r"C:\Users\Nathan Nangle\Desktop\Lab 4\Github Calc\ballisticsolver\G1 Drag Function.csv") as G1DragFile:
            G1Drag = list(csv.reader(G1DragFile))
            # Used for interpolation y = (y1-y0)/(x1-x0)*(x-x0)+y0
            x_values = []
            y_values = []
            bottom_index = 0

            for row in G1Drag:
                velocity_table = float(row[0]) * mach_conversion
                #print("vel table: ", velocity_table)
                if velocity - velocity_table == 0:
                    #print("here 1")
                    return row[1]
                elif velocity - velocity_table > 0:
                    #print("here 2")

                    bottom_index += 1
                elif velocity - velocity_table < 0:
                    #print("here 3")
                    top_index = bottom_index
                    x_values.append(float(G1Drag[bottom_index - 1][0]) * mach_conversion)
                    x_values.append(float(G1Drag[top_index][0]) * mach_conversion)
                    y_values.append(float(G1Drag[bottom_index - 1][1]))
                    y_values.append(float(G1Drag[top_index][1]))
                    # print(bottom_index)
                    # print(top_index)
                    # print (x_values)
                    # print (y_values)
                    # print (velocity)
                    cd = (y_values[1] - y_values[0]) / (x_values[1] - x_values[0]) * (velocity - x_values[0]) + y_values[0]
                    #print("cd: ", cd)
                    return cd


# ---------------------------------------------------------------------------------------------------------------------------

def main():
    bullet = [None, None, None, None, None]  # bullet[caliber, grainage, G1, velocity, range]
    atmosphere = [None, None, None, None, None]  # atmosphere[crosswind, direction, elevation, windage]

    ready = False
    while ready == False:


        bullet = [0.308, 110, 0.49, 1014, 92]  # bullet[caliber, grainage, G1, velocity, range]
        atmosphere = [20, 0, 0,0,1.183]  # atmosphere[crosswind, direction, elevation, windage]

        ready = True

    trajectoryGraph(bullet, atmosphere)


if __name__ == "__main__":
    main()

    # while bullet[0] == None:
    #     bullet[0] = input("please enter bullet caliber: ")
    #     bullet[0] = float(bullet[0])
    # while bullet[1] == None:
    #     bullet[1] = input("please enter bullet grainage: ")
    #     bullet[1] = int(bullet[1])
    # while bullet[2] == None:
    #     bullet[2] = input("please enter bullet G1 coefficient: ")
    #     bullet[2] = float(bullet[2])
    # while bullet[3] == None:
    #     bullet[3] = input("please enter bullet muzzle velocity: ")
    #     bullet[3] = int(bullet[3])
    # while bullet[4] == None:
    #     bullet[4] = input("please enter target range: ")
    #     bullet[4] = int(bullet[4])
    #
    # while atmosphere[0] == None:
    #     atmosphere[0] = input("please enter crosswind: ")
    #     atmosphere[0] = int(atmosphere[0])
    # while atmosphere[1] == None:
    #     atmosphere[1] = input("please enter crosswind direction: ")
    #     atmosphere[1] = int(atmosphere[1])
    # while atmosphere[2] == None:
    #     atmosphere[2] = input("please enter elevation: ")
    #     atmosphere[2] = int(atmosphere[2])
    # while atmosphere[3] == None:
    #     atmosphere[3] = input("please enter windage: ")
    #     atmosphere[3] = int(atmosphere[3])
    # while atmosphere[4] == None:
    #     atmosphere[4] = input("please enter air density: ")
    #     atmosphere[4] = float(atmosphere[4])