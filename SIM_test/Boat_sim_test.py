import pygame as pg


import math
import random
import numpy as np
from scipy.interpolate import interp1d


pg.init()


width_aspect=16
heigth_aspect=9

cell_size=90
window_size=[cell_size*width_aspect,cell_size*heigth_aspect]

water_color=[140, 200, 255]

screen = pg.display.set_mode(window_size,pg.SHOWN)
pg.display.set_caption("Sail Boat Simulation Test")

player_boat_img=pg.image.load("IMG/player_boat.png")
player_boat_img.convert()

class boat:
  def __init__(self,pos,angle,size,color):
    self.pos=pos
    self.vel=[0,0]
    self.acc=[0,0]

    self.angle = angle
    self.angle_vel=0
    self.angle_acc=0

    self.size = size

    self.boat = None
    self.boat_rect = None

    self.scale_factor=1
    
    self.color=color

    self.wind_angles=np.array([0,5,10,15,20,25,32,36,40,45,52,60,70,80,90,100,110,120,130,140,150,160,170,180])
    self.speeds_line=[0.0, 0.5, 1.1, 1.6, 1.9, 2.2, 3.7, 4.3, 4.8, 5.2, 5.3, 6.2, 6.4, 6.6, 6.8, 6.8, 6.7, 6.4, 5.8, 5.2, 4.6, 4.0, 3.6, 3.4]

    self.f_speed = interp1d(self.wind_angles, self.speeds_line, kind='cubic')

  def setImg(self,img):
    self.scale_factor = self.size / img.get_width()
    self.boat = img

  def show(self,angleOffset):
    boat_img = pg.transform.rotozoom(self.boat, (-self.angle+angleOffset), self.scale_factor)
    self.boat_rect = boat_img.get_rect()
    self.boat_rect.center = self.pos
    tinted_boat = boat_img.copy()
    tinted_boat.fill(self.color, special_flags=pg.BLEND_RGB_MULT)
    screen.blit(tinted_boat, self.boat_rect)
  
  def turn(self,turn_strength,max_angle_vel=1):
    self.angle_acc =  (max_angle_vel - abs(self.angle_vel))*turn_strength

  def sail(self,max_speed,strength):
    
    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))

    forward_speed = self.vel[0]*fx + self.vel[1]*fy

    speed_error = max_speed - forward_speed

    
    self.acc[0] += fx * speed_error * strength
    self.acc[1] += fy * speed_error * strength

    print(speed_error)

    

  def getBoatSpeed(self,wind_speed,wind_angle,scala=1):

    return self.f_speed(self.rel_angle(wind_angle,self.angle))*wind_speed*scala

  def rel_angle(self,wind_angle,boat_angle):
    delta = (wind_angle - boat_angle) % 360
    return delta if delta <= 180 else 360 - delta

  def update(self):
    # rotation
    self.angle_vel += self.angle_acc
    self.angle += self.angle_vel
    self.angle_vel *= 0.99

    # apply acceleration to velocity
    self.vel[0] += self.acc[0]
    self.vel[1] += self.acc[1]


    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))
    sx = -fy
    sy = fx

    # remove sideways drift
    sideways_speed = self.vel[0]*sx + self.vel[1]*sy
    self.vel[0] -= sx * sideways_speed * 0.01
    self.vel[1] -= sy * sideways_speed * 0.01

    self.vel[0] *= 0.9999
    self.vel[1] *= 0.9999

    # --- now move ---
    self.pos[0] += self.vel[0]
    self.pos[1] += self.vel[1]

    # reset
    self.angle_acc = 0
    self.acc = [0,0]



player_boat=boat([100,100],90,85,[200,200,100])
player_boat.setImg(player_boat_img)

run=True

while run:
  events = pg.event.get()
  screen.fill((water_color))

  key= pg.key.get_pressed()


  if key[pg.K_ESCAPE]:
    run = False

  if key[pg.K_a]:
    player_boat.turn(-0.003)
  if key[pg.K_d]:
    player_boat.turn(0.003)

  if key[pg.K_w]:
    player_boat.sail(0,0.001)
  else:
    
    player_boat.sail(player_boat.getBoatSpeed(15,270,0.005),0.002)

  player_boat.update()

  for event in events:
    if event.type==pg.QUIT:
      run = False

  player_boat.show(90)

  pg.display.update()







pg.quit()