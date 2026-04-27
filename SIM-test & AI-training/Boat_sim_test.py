import pygame as pg

import random as r
import math
import numpy as np

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


player_boat=boat([window_size[0]/2,window_size[1]/2],r.randrange(20,40))
player_boat.setColor([200,200,200])
player_boat.setSize(65)
player_boat.setImg(player_boat_img)
player_boat.setFPS(300)

wind_angles=[0,5,10,15,20,25,32,36,40,45,52,60,70,80,90,100,110,120,130,140,150,160,170,180]
speeds=[0.0, 0.5, 1.1, 1.4, 1.9, 2.4, 3.7, 4.3, 4.8, 5.2, 5.8, 6.2, 6.4, 6.6, 6.8, 6.8, 6.7, 6.4, 5.8, 5.2, 4.6, 4.0, 3.6, 3.4]

player_boat.setsSailData(wind_angles,speeds)
player_boat.setWindowSize(window_size)

run=True

font = pg.font.SysFont('mono', 20,True,False)

player_boat.setPointsSettings(270,290,120,6)

track =[[8,4.5],[9.4,2.1],[12.6,2.1],
        [13.5,4.3],[11,5.5],[13.5,6.6],
        [6.8,7],[5.3,4.4],[3.1,4.8],
        [5.2,6.1],[2.3,6.9],[2.1,2.2]]

for i in range(len(track)):
  track[i][0]*=cell_size
  track[i][1]*=cell_size

player_boat.generatePoints()
turnStrength = 5
maxTurnVel = 175

player_boat.setMaxAngleVel(maxTurnVel)
player_boat.setTurnStrength(turnStrength)
player_boat.setSidewaysGrip(5)
player_boat.setSpeedScala(2)
player_boat.setSailAccStrength(0.75)
player_boat.setPointReward(10000)
player_boat.setLimit(window_size)
player_boat.setWind(15,270)

while run:
  events = pg.event.get()
  screen.fill((water_color))

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  if key[pg.K_r]:
    player_boat.reset([window_size[0]/2,window_size[1]/2],r.randrange(0,359),r.randrange(10,20,5),r.randrange(0,359))

  if key[pg.K_a]:
    player_boat.turn(0)
  if key[pg.K_d]:
    player_boat.turn(1)

  if key[pg.K_w]:
    player_boat.sail(False)
  else:
    player_boat.sail()

  player_boat.getDirVectors()
  player_boat.update()

  for event in events:
    if event.type==pg.QUIT:
      run = False

  player_boat.show(90,screen)
  player_boat.getTargetPoint(20,True)
  player_boat.drawPoints(screen,font)


  pg.display.update()




pg.quit()