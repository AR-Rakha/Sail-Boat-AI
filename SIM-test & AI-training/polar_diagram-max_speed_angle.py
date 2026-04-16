import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


wind_angles=[0,5,10,15,20,25,32,36,40,45,52,60,70,80,90,100,110,120,130,140,150,160,170,180,
             190,200,210,220,230,240,250,260,270,280,290,300,308,315,320,324,328,335,340,345,350,355,360]
wind_speeds=[0,4,6,8,10,12,14,16,20,25,30,35,40,45,50,55,60]
speed_0=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
speed_1=[0.0, 0.4, 0.7, 1.1, 1.2, 1.4, 2.4, 2.7, 3.2, 3.5, 4.0, 4.4, 4.5, 4.7, 4.9, 4.9, 4.9, 4.5, 4.1, 3.5, 3.0, 2.7, 2.3, 2.2]
speed_2=[0.0, 0.5, 1.1, 1.6, 1.9, 2.2, 3.7, 4.3, 4.8, 5.2, 5.3, 6.2, 6.4, 6.6, 6.8, 6.8, 6.7, 6.4, 5.8, 5.2, 4.6, 4.0, 3.6, 3.4]
speed_3=[0.0, 0.6, 1.2, 1.8, 2.0, 2.4, 4.0, 4.4, 4.8, 5.5, 5.8, 7.2, 7.4, 7.6, 7.9, 7.8, 7.7, 7.5, 7.1, 6.5, 5.8, 5.1, 4.6, 4.4]
speed_4=[0.0, 0.7, 1.4, 2.2, 2.5, 2.9, 4.9, 5.4, 6.0, 6.4, 7.0, 7.6, 7.8, 7.9, 8.0, 8.1, 8.3, 8.5, 8.4, 8.1, 7.7, 6.9, 6.4, 6.0]
speed_5=[0.0, 0.9, 1.8, 2.8, 3.2, 3.8, 6.3, 6.9, 7.3, 7.6, 7.9, 8.2, 8.4, 8.5, 8.5, 8.8, 9.1, 8.9, 8.5, 8.0, 7.6, 7.1, 6.6, 6.3]
speed_6=[0.0, 1.0, 2.0, 3.0, 3.4, 4.1, 6.8, 7.2, 7.6, 7.9, 8.1, 8.4, 8.7, 8.9, 8.9, 9.2, 9.5, 9.7, 9.1, 8.6, 8.1, 7.8, 7.4, 7.1]
speed_7=[0.0, 1.0, 2.0, 3.1, 3.5, 4.2, 7.0, 7.5, 7.7, 8.0, 8.2, 8.6, 8.9, 9.2, 9.4, 9.6, 9.8, 10.1, 9.7, 9.2, 8.6, 8.2, 7.9, 7.6]
speed_8=[0.0, 1.1, 2.1, 3.2, 3.6, 4.3, 7.2, 7.5, 7.8, 8.0, 8.4, 8.7, 9.1, 9.5, 10.0, 10.2, 10.3, 10.9, 11.4, 11.1, 10.0, 9.5, 9.2, 8.9]
speed_9=[0.0, 1.1, 2.1,	3.2, 3.7, 4.4, 7.3, 7.6, 7.9, 8.2, 8.6, 8.9, 9.3, 9.9, 10.6, 11.2, 12.2, 12.0, 13.0, 13.9, 12.3, 11.3,	10.6, 10.1]
speed_10=[0.0, 1.1, 2.1, 3.2, 3.6, 4.3, 7.2, 7.6, 7.9, 8.3, 8.7, 9.0, 9.6, 10.4, 11.3, 12.1, 13.5, 14.2, 14.5, 16.4, 15.5, 13.9, 12.6, 12.0]
speed_11=[0.0, 1.0, 2.0, 2.9, 3.4, 4.0, 6.7, 7.5, 7.8, 8.2, 8.7, 9.1, 9.8, 10.6, 11.7, 12.7, 14.4, 15.6, 16.6, 18.1, 18.2, 17.3, 15.6, 14.6]
speed_12=[0.0, 0.1, 0.5, 1.0, 1.6, 2.3, 5.0, 6.2, 6.9, 7.8, 8.5, 9.1, 9.8, 10.6, 11.7, 12.7, 14.4, 15.6, 16.6, 18.1, 18.2, 17.3, 15.6, 14.6]
speed_13=[0.0, 0.1, 0.2, 0.4, 0.7, 1.0, 2.0, 2.5, 2.7, 2.9, 3.0, 3.6, 3.9, 4.2, 5.3, 6.4, 7.9, 9.4, 10.8,	13.6,	14.6,	14.7,	14.8,	14.6]
speed_14=[0.0, 0.1, 0.2, 0.3, 0.3, 0.4, 0.7, 0.8, 1.2, 1.2, 1.3, 1.8, 2.0, 2.1, 2.9, 3.8, 5.0, 6.2, 7.5, 10.0,	10.9,	11.2,	11.7,	11.7]
speed_15=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.6, 1.4, 1.6, 2.5, 3.6, 3.6, 4.3, 4.7, 4.4]
speed_16=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.6, 1.4, 1.6, 2.5, 2.7, 3.6, 3.5, 3.9, 3.7]
speeds=[speed_0,speed_1,speed_2,speed_3,speed_4,speed_5,speed_6,speed_7,speed_8,speed_9,speed_10,speed_11,speed_12,speed_13,speed_14,speed_15,speed_16]

all_speeds=speeds
#print(speeds)

#print(np.asarray(wind_angles)+180)

for s in range(len(speeds)):
  all_speeds[s].extend(list(reversed(speeds[s][:-1])))





# Specifying polar coordinates
theta = np.linspace(0, 2*np.pi, len(speed_0))
r = [0.2, 0.5, 0.8, 1.2, 1.5, 1.8, 2.1, 2.5, 2.8, 3.0, 2.8, 2.5, 2.1, 1.8, 1.5, 1.2, 0.8, 0.5, 0.2, 0.0]

# Creating a polar scatter plot with data points
'''for w in range(0,len(all_speeds)):
  plt.polar(np.asarray(wind_angles)*np.pi/180, speeds[w], marker='o', linestyle='solid',lw=1,ms=2, label=str(wind_speeds[w])+" knots")
plt.legend(bbox_to_anchor=(1.5, 1))
plt.show()'''

# Choose one speed line, e.g., speed_2
sp = 2
angles = np.array(wind_angles)  # full 0-360 angles
speeds_line = np.array(speeds[sp])
my_speeds_line = [0.0, 0.5, 1.1, 1.4, 1.9, 2.4, 3.7, 4.3, 4.8, 5.2, 5.8, 6.2, 6.4, 6.6, 6.8, 6.8, 6.7, 6.4, 5.8, 5.2, 4.6, 4.0, 3.6, 3.4]

my_speeds_line.extend(list(reversed(my_speeds_line[:-1])))

my_speeds_line = np.array(my_speeds_line)

'''plt.polar(np.asarray(wind_angles)*np.pi/180, speeds[sp], marker='o', linestyle='solid',lw=1,ms=2, label=str(wind_speeds[sp])+" knots")
plt.legend(bbox_to_anchor=(1.5, 1))
plt.show()'''


# Interpolation
f_speed = interp1d(angles, my_speeds_line, kind='cubic')

def rel_angle(wind_angle,boat_angle):
  return (wind_angle - boat_angle) % 360

print(f_speed(rel_angle(90,0)))

# Smooth angles for plotting
theta_deg = np.linspace(0, 360, 360)
theta_rad = np.radians(theta_deg)
r = f_speed(theta_deg)

# Plot
plt.figure(figsize=(7,7))
ax = plt.subplot(111, polar=True)
ax.plot(theta_rad, r, linestyle='solid', marker=None)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
plt.title(f"Boat speed vs wind angle ({wind_speeds[sp]} knots)")
plt.show() 