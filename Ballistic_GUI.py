from tkinter import *
#from PIL import Image
import time
import math
import SimulatedConditions
import Ballistics
#---------------------------------------------------------------------------------------------------------------

def raise_frame(frame):
    frame.tkraise()

#---------------------------------------------------------------------------------------------------------------

def AddWindDir(current_wind):
    new_windD = current_wind + 1
    return new_windD
    
def SubWindDir(current_wind):
    new_windD = current_wind - 1
    return new_windD
    
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
    feet = 2
    inches = feet*12
    scale_factor = 1
    size = 10 * 12 * feet * scale_factor
    canvas_w = size
    canvas_h = size

    x = (size / 2) - 2.5
    x1 = (size / 2) + 2.5
    y = (size / 2) - 2.5
    y1 = (size / 2) + 2.5

    simlist = SimulatedConditions.LoadData()
    first_iteration = True
    iframe1 = Frame(f2, relief=RAISED, bd=2)
    iframe1.grid(column=10, row=13)
    c = Canvas(iframe1, bg='white', width=canvas_w, height=canvas_h)

    c.grid(column=10, row=12)

    c.create_line((size/2), 0, (size/2), size)
    c.create_line(0, (size/2), size, (size/2))

    #create a hash mark every inch on x-y
    steps = 10 * scale_factor
    sizer = 5 * scale_factor
    for k in range(0, canvas_w, steps):
        c.create_line(((size/2) - sizer), k, ((size/2) + sizer), k) #y hash
        c.create_line(k, ((size/2) - sizer), k, ((size/2) + sizer)) #x hash
    
    hash_counter = 1
    for f in range(10, int(canvas_w/2), steps):
        #x hash measurement
        c.create_text(((size / 2) - f), ((size/2) + 10), text = str(hash_counter), font = ("Arial", 5))
        c.create_text(((size / 2) + f), ((size/2) + 10), text = str(hash_counter), font = ("Arial", 5))
        
        #y hash measurement
        c.create_text(((size/2) + 10), ((size / 2) - f), text = str(hash_counter), font = ("Arial", 5))
        c.create_text(((size/2) + 10), ((size / 2) + f), text = str(hash_counter), font = ("Arial", 5))
    
        hash_counter += 1

    c.create_text(((size/2) - 20), 10, text = "90")
    c.create_text(((size) - 10), ((size/2) - 20), text = "0")
    c.create_text(((size/2) - 20), ((size) - 10), text = "270")
    c.create_text(10, ((size/2) - 20), text = "180")

    mover = c.create_oval(x, y, x1, y1, fill="red") #where bullet will land if aim is directly at center
    inverse_mover = c.create_oval(x, y, x1, y1, fill="blue") #where to aim
    
    #aids visual tracking, dynamically moving line
    mover_line_x = c.create_line((size/2), ((size/2) - 7), (size/2), ((size/2) + 7), fill = "red")
    mover_line_y = c.create_line(((size/2) - 7), (size/2), ((size/2) + 7), (size/2), fill = "red")
    inv_mover_line_x = c.create_line((size / 2), ((size / 2) - 7), (size / 2), ((size / 2) + 7), fill="blue")
    inv_mover_line_y = c.create_line(((size / 2) - 7), (size / 2), ((size / 2) + 7), (size / 2), fill="blue")
    
    ball_pos = [0,0]
    count = 0
    current_dir = 45
    while 1:
        deflection1 = []
        windspeed = float(SimulatedConditions.windspeed(count, simlist))
        winddir = float(SimulatedConditions.winddir(count))
        density = 1.183
        print("wind d: ", winddir, " / ", count)

        Label(f2, text = "wind speed is currently (MPH): ").grid(column= 1, row=6)
        Label(f2, text= windspeed).grid(column=2, row=6)
        
        atmosphere = [windspeed, winddir, 0, 0, density]

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
        
        move_x = BulletPhysicsWind(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere,f2)
        move_y = BulletPhysicsGravity(size, int(target_range), first_iteration, ball_pos, bullet, atmosphere,f2)

        Label(f2, text="horizontal deflection: ").grid(column=1, row=11)
        Label(f2, text=str(round(move_x[0], 2))).grid(column=2, row=11)
        
        Label(f2, text="vertical deflection: ").grid(column=1, row=12)
        Label(f2, text=str(round(move_y[0], 2))).grid(column=2, row=12)

        c.move(mover, move_x[1], move_y[1])  # , ball_pos)
        c.move(inverse_mover, -move_x[1], -move_y[1])  # , ball_pos)

        c.move(mover_line_x, move_x[1], 0)
        c.move(mover_line_y, 0, move_y[1])

        c.move(inv_mover_line_x, -move_x[1], 0)
        c.move(inv_mover_line_y, 0, -move_y[1])
        
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

def BulletPhysicsWind(size, range1, iteration, position, bullet, atmosphere,f2): # atmosphere[crosswind, direction, elevation, windage, density]
    target_size = size/12
    deflection1 = Ballistics.trajectoryGraph(bullet, atmosphere) #-(wind_vect * (((test_time) - (range1 / speed)))) #deflection goes in the opposite direction of the wind direction
    deflection1.sort()
    x_movement = [0,0]

    deflection = (-1)*deflection1[1]
    x_movement[0] = deflection
    
    def_2_pix = (deflection / target_size) * size
    int_def_2_pix = int(def_2_pix)

    position_vector_old = position[0] - (size/2)  # old position distance from y-axis
    position_vector_new = (int_def_2_pix + (size/2)) - (size/2)  # if (+) right side of y-ax; if (-) left side of y-ax

    if(iteration): # if it is the first iteration return the full deflection
        x_movement[1] = def_2_pix
        return x_movement

    elif(iteration == False and position_vector_old < position_vector_new):  # if it isnt the first iter & the deflection than before is more calculate new deflection and add the difference
        def_diff = abs(position_vector_new - position_vector_old)            # ex) old = -7; new = -5; dist = 2; move 2 right
                                                                             # need to add diffence in deflection to account for drift
        x_movement[1] = def_diff
        return x_movement


    elif (iteration == False and position_vector_old > position_vector_new): # if it isnt the first iter & the deflection is less than before calculate new deflection and sub the difference
        def_diff = abs(position_vector_old - position_vector_new)            # ex) old = -5; new = -7 dist = 2; move 2 left
                                                                             # need to sub diffence in deflection to account for drift
        x_movement[1] = -def_diff
        return x_movement

    else:                                                                    # if it isnt the first iter & the def hasnt changed
        def_2_pix = 0                                                        # return 0 for no change on graph
        x_movement[1] = def_2_pix
        return x_movement

# ---------------------------------------------------------------------------------------------------------------

def BulletPhysicsGravity(size, range1, iteration, position, bullet, atmosphere, f2): #assuming no friction
    target_size = size/12 #target size inches
    y_movement = [0,0]
    
    deflection1 = Ballistics.trajectoryGraph(bullet, atmosphere)
    y_movement[0] = deflection1[0]

    drop_2_pix = -(deflection1[0] / target_size) * size
    int_drop_2_pix = int(drop_2_pix)

    position_vector_old = position[1] - (size / 2)  # old position distance from x-axis
    position_vector_new = (int_drop_2_pix + (size / 2)) - (size / 2)  # if (+) right side of x-ax; if (-) left side of x-ax
    
    if(iteration):              # if first iteration, move down
        y_movement[1] = int(drop_2_pix)
        return y_movement
        #return int(drop_2_pix)
    
    elif(iteration == False and position_vector_old < position_vector_new):
        def_diff = abs(position_vector_new - position_vector_old)
        y_movement[1] = def_diff
        return y_movement
    
    elif (iteration == False and position_vector_old > position_vector_new):
        def_diff = abs(position_vector_old - position_vector_new)
        y_movement[1] = def_diff
        return y_movement
    
    else:                       # return 0 so animation doesnt continue to fall (change later)
        def_2_pix = 0  # return 0 for no change on graph
        y_movement[1] = def_2_pix
        return y_movement

# ---------------------------------------------------------------------------------------------------------------
root = Tk()

f1 = Frame(root)
f2 = Frame(root)

for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')
root.title("Ballistic Calculator")
root.geometry("650x550")

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