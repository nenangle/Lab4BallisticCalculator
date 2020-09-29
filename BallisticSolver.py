import math
from pyowm import OWM

owm = OWM('e25bdad854e824073fcecada0ae302c2')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Lubbock, US')
w = observation.weather
print(w.wind())                  # <Weather - reference time=2013-12-18 09:20, status=Clouds>

# Weather details
w.wind()                  # {'speed': 4.6, 'deg': 330}

# bullet_speed = 1500  # fps
# target_dist = 100  # yards
# travel_time = (target_dist * 3) / bullet_speed  # t = d / v
# drop = 0.5 * (32.185) * (travel_time*travel_time)
# drop_2_pix = (drop / 24)*200
# print("Drop is: ", drop)
# print("Drop to pixels is: ", drop_2_pix)
#
# wind = 10
# angle = 90
# angle_rads = angle*(3.1415/180)
#
# wind_vect = 10*math.cos(angle_rads)
# deflection = wind_vect*((0.214)-(target_dist/1500))
# print("wind magnitude is: ", wind_vect)
# print("Deflection is: ", deflection)