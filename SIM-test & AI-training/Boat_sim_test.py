import pygame as pg

import random
import math
import numpy as np
from scipy.interpolate import interp1d

from Boat_Class import boat


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


player_boat=boat([100,100],90,65,[200,200,100])
player_boat.setImg(player_boat_img)

run=True

points=[[random.randrange(0+90,window_size[0]-90),random.randrange(0+90,window_size[1]-90)]]
for x in range(9):
  randP=[random.randrange(0+90,window_size[0]-90),random.randrange(0+90,window_size[1]-90)]
  toClose=False
  for d in range(len(points)):
    if math.sqrt((points[d][0]-randP[0])**2+(points[d][1]-randP[1])**2)<180:
      toClose=True
      break
    
  while toClose:
    toClose=False
    randP=[random.randrange(0+90,window_size[0]-90),random.randrange(0+90,window_size[1]-90)]
    for d in range(len(points)):
      if math.sqrt((points[d][0]-randP[0])**2+(points[d][1]-randP[1])**2)<90:
        toClose=True
        break

  points.append(randP.copy())

font = pg.font.SysFont('mono', 20,True,False)


while run:
  events = pg.event.get()
  screen.fill((water_color))

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  if key[pg.K_a]:
    player_boat.turn(-0.004)
  if key[pg.K_d]:
    player_boat.turn(0.004)

  if key[pg.K_w]:
    player_boat.sail(0,0.001)
  else:
    
    player_boat.sail(player_boat.getBoatSpeed(15,270,0.005),0.002)

  player_boat.update()

  for event in events:
    if event.type==pg.QUIT:
      run = False

  player_boat.show(90,screen)
  for x in range(len(points)):
    pg.draw.circle(screen, (0,0,0), (points[x][0],points[x][1]), 15)
    textImg = font.render(str(x+1), True, (255,255,255))
    text_width, text_height = font.size(str(x+1)) #txt being whatever str you're rendering
    screen.blit(textImg, (points[x][0]-text_width/2,points[x][1]-text_height/2))


  pg.display.update()




pg.quit()