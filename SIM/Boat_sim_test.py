import pygame as pg


import math
import random


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

    print(forward_speed)

  def update(self):
    # rotation
    self.angle_vel += self.angle_acc
    self.angle += self.angle_vel
    self.angle_vel *= 0.95

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

    self.vel[0] *= 1
    self.vel[1] *= 1

    # --- now move ---
    self.pos[0] += self.vel[0]
    self.pos[1] += self.vel[1]

    # reset
    self.angle_acc = 0
    self.acc = [0,0]

player_boat=boat([100,100],90,100,[200,200,200])
player_boat.setImg(player_boat_img)

run=True

while run:
  events = pg.event.get()
  screen.fill((water_color))

  key= pg.key.get_pressed()


  if key[pg.K_ESCAPE]:
    run = False

  if key[pg.K_a]:
    player_boat.turn(-0.01)
  if key[pg.K_d]:
    player_boat.turn(0.01)

  if key[pg.K_w]:
    player_boat.sail(0,0.001)
  else:
    player_boat.sail(0.5,0.005)

  player_boat.update()

  for event in events:
    if event.type==pg.QUIT:
      run = False

  player_boat.show(90)

  pg.display.update()







pg.quit()