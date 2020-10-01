from tkinter import *
from PIL import Image
import time
import math
import SimulatedConditions
import Ballistics
#---------------------------------------------------------------------------------------------------------------

def raise_frame(frame):
    frame.tkraise()

#---------------------------------------------------------------------------------------------------------------

def Frame2Attributes(f2, cal, dia, coef, speed, dist):
    raise_frame(f2)
    cal_text = "your caliber: " + str(cal)
    dia_text = "your grainage: " + str(dia)
    coef_text = "your coefficient: " + str(coef)
    dist_text = "muzzle velocity (FPS): " + str(speed)
    range_text = "target range (yards): " + str(dist)

    # bullet[caliber, grainage, G1, velocity, range]
    bullet = [float(cal), int(dia), float(coef), int(speed), int(dist)]
    # atmosphere[crosswind, direction, elevation, windage, density]

    Label(f2, text = cal_text).grid(column = 1, row = 1)
    Label(f2, text = dia_text).grid(column = 1, row = 2)
    Label(f2, text = coef_text).grid(column = 1, row = 3)
    Label(f2, text = dist_text).grid(column = 2, row = 1)
    Label(f2, text = range_text).grid(column = 2, row = 2)

    Label(f2, text= "Atmospheric Conditions").grid(column= 2, row=5)

    Button(f2, text = 'Start Logging', command = lambda:Frame2DynamicAttributes(speed, dist, bullet)).grid(column = 1, row = 4)#(ShotAnimation(), Frame2DynamicAttributes())).grid(column = 1, row = 4)

#---------------------------------------------------------------------------------------------------------------

def Frame2DynamicAttributes(bullet_speed, target_range, bullet):
    canvas_w = 200  # 2 x 2 feet
    canvas_h = 200
    x = 95
    x1 = 105
    y = 95
    y1 = 105
    simlist = SimulatedConditions.LoadData()
    first_iteration = True
    iframe1 = Frame(f2, relief=RAISED, bd=2)
    iframe1.grid(column=10, row=12)
    c = Canvas(iframe1, bg='white', width=canvas_w, height=canvas_h)
    c.grid(column=10, row=12)
    c.create_line(100, 0, 100, 200)
    c.create_line(0, 100, 200, 100)

    c.create_text(90, 10, text = "90")
    c.create_text(190, 110, text = "0")
    c.create_text(90, 190, text = "270")
    c.create_text(10, 110, text = "180")

    mover = c.create_oval(x, y, x1, y1, fill="red")
    ball_pos = [0,0]
    count = 2
    while 1:
        deflection1 = []
        windspeed = float(SimulatedConditions.windspeed(count, simlist))
        winddir = int(SimulatedConditions.winddir())
        density = 1.183
        atmosphere = [windspeed, winddir, 0, 0, density]


        Label(f2, text = "wind speed is currently (MPH): ").grid(column= 1, row=6)
        Label(f2, text= windspeed).grid(column=2, row=6)


        Label(f2, text="wind direction is currently (deg): ").grid(column=1, row=7)
        Label(f2, text=winddir).grid(column=2, row=7)

        temp = SimulatedConditions.temp()
        Label(f2, text="temperature is currently (deg F): ").grid(column=1, row=8)
        Label(f2, text=temp).grid(column=2, row=8)

        humidity = SimulatedConditions.hum()
        Label(f2, text="humidity is currently (%): ").grid(column=1, row=9)
        Label(f2, text=humidity).grid(column=2, row=9)

        pressure = SimulatedConditions.pres()
        Label(f2, text="pressure is currently (inHg): ").grid(column=1, row=10)
        Label(f2, text=pressure).grid(column=2, row=10)

        move_x = BulletPhysicsWind(int(bullet_speed), int(target_range), first_iteration, ball_pos, bullet, atmosphere,f2)


        move_y = BulletPhysicsGravity(int(bullet_speed), int(target_range), first_iteration, ball_pos, bullet, atmosphere,f2)
        c.move(mover, move_x, move_y) #, ball_pos)
        ball_pos = BallCenter(c.coords(mover))
        print("Cords are: ", ball_pos)
        first_iteration = False
        time.sleep(.01)
        root.update()
        count += 1
#---------------------------------------------------------------------------------------------------------------
def BallCenter(coor):
    x = (coor[0] + coor[2])/2
    y = (coor[1] + coor[3])/2
    cord = [x,y]
    return cord

# ---------------------------------------------------------------------------------------------------------------

def BulletPhysicsWind(speed, range1, iteration, position, bullet, atmosphere,f2): # atmosphere[crosswind, direction, elevation, windage, density]

    # test_speed = speed - speed*(range1/1000)
    # test_time = (range1*3) / test_speed
    # print("test speed/time: ", test_speed, " / ", test_time)
    # wind_vect = windspeed * math.cos(math.radians(winddir))
    deflection1 = Ballistics.trajectoryGraph(bullet, atmosphere) #-(wind_vect * (((test_time) - (range1 / speed)))) #deflection goes in the opposite direction of the wind direction

    deflection1.sort()

    Label(f2, text="horizontal deflection: ").grid(column=1, row=11)
    Label(f2, text=deflection1[1]).grid(column=2, row=11)

    deflection = (-1)*deflection1[1]
    def_2_pix = (deflection / 24) * 200

    int_def_2_pix = int(def_2_pix)

    # print("pixels value ", int_def_2_pix)
    # print("position value ", position)

    position_vector_old = position[0] - 100   # old position distance from y-axis
    # print("old position vector: ", position_vector_old)

    position_vector_new = (int_def_2_pix + 100) - 100 # if (+) right side of y-ax; if (-) left side of y-ax
    # print("new position vector: ", position_vector_new)


    if(iteration): # if it is the first iteration return the full deflection
        return def_2_pix

    elif(iteration == False and position_vector_old < position_vector_new):  # if it isnt the first iter & the deflection than before is more calculate new deflection and add the difference
        def_diff = abs(position_vector_new - position_vector_old)            # ex) old = -7; new = -5; dist = 2; move 2 right
        # print("deflection change: ", def_diff)                               # need to add diffence in deflection to account for drift

        return def_diff

    elif (iteration == False and position_vector_old > position_vector_new): # if it isnt the first iter & the deflection is less than before calculate new deflection and sub the difference
        def_diff = abs(position_vector_old - position_vector_new)            # ex) old = -5; new = -7 dist = 2; move 2 left
        # print("deflection change1: ", def_diff)                              # need to sub diffence in deflection to account for drift

        return -def_diff

    else:                                                                    # if it isnt the first iter & the def hasnt changed
        def_2_pix = 0                                                        # return 0 for no change on graph
        return def_2_pix

# ---------------------------------------------------------------------------------------------------------------

def BulletPhysicsGravity(speed, range1, iteration, position, bullet, atmosphere, f2): #assuming no friction
    test_speed = speed - speed * (range1 / 1000)
    travel_time = (range1 * 3) / test_speed  # t = d / v

    drop = 0.5 * (32.185) * (travel_time * travel_time)

    deflection1 = Ballistics.trajectoryGraph(bullet, atmosphere)

    Label(f2, text="vertical deflection: ").grid(column=1, row=12)
    Label(f2, text=deflection1[0]).grid(column=2, row=12)

    drop_2_pix = -(deflection1[0] / 24) * 200
    if(iteration):              # if first iteration, move down
        return int(drop_2_pix)
    else:                       # return 0 so animation doesnt continue to fall (change later)
        return 0

# ---------------------------------------------------------------------------------------------------------------
root = Tk()

f1 = Frame(root)
f2 = Frame(root)

for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')
root.title("Ballistic Calculator")
root.geometry("600x500")

Label(f1, text='Enter Bullet Diameter (in)').grid(column = 1, row = 1)
cal_entry = Entry(f1,width = 5)
cal_entry.insert(0,'0.308')
cal_entry.grid(column = 2, row = 1)

Label(f1, text='Enter Bullet Grain').grid(column = 1, row = 2)
bullet_entry = Entry(f1,width = 5)
bullet_entry.insert(0,'110')
bullet_entry.grid(column = 2, row = 2)

Label(f1, text='Enter Ballistic Coefficient (G1)').grid(column = 1, row = 3)
ballistic_entry = Entry(f1,width = 5)
ballistic_entry.insert(0,'0.29')
ballistic_entry.grid(column = 2, row = 3)

Label(f1, text='Enter Bullet Velocity (FPS)').grid(column = 1, row = 4)
velocity_entry = Entry(f1,width = 5)
velocity_entry.insert(0,'2500')
velocity_entry.grid(column = 2, row = 4)

Label(f1, text='Enter Target Distance (yards)').grid(column = 1, row = 5)
distance_entry = Entry(f1,width = 5)
distance_entry.insert(0,'100')
distance_entry.grid(column = 2, row = 5)

Label(f1, text='Press Enter When Done').grid(column = 1, row = 6)
Button(f1, text='Enter', command=lambda:Frame2Attributes(f2, cal_entry.get(), bullet_entry.get(), ballistic_entry.get(), velocity_entry.get(), distance_entry.get())).grid(column = 2, row = 6)


raise_frame(f1)
root.mainloop()