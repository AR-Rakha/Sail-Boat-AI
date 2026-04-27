import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

import math
import random as r

from BoatClass import boat


pg.init()

width_aspect=16
heigth_aspect=9

cell_size=90
cell_gap=10

window_size=[cell_size*width_aspect,cell_size*heigth_aspect]

water_color=[140, 200, 255]

font = pg.font.SysFont('mono', 20,True,False)

screen = pg.display.set_mode(window_size,pg.SHOWN)
pg.display.set_caption("SAILBOAT AI - MAIN")

def widget_on_off_Y(button,posX,posY,offset,c_widgets,c_widget_offsets,widgets=[],widget_offsets=[],p_widgets=[],p_widget_offsets=[]):
  button.on = not getattr(button, "on", False)

  if button.on:
    button.setY(posY + offset[1]*cell_size)
    for i in range(len(c_widgets)):
      c_widgets[i].move_ip(cell_size*c_widget_offsets[i][0], cell_size*c_widget_offsets[i][1])
    for i in range(len(widgets)):
      widgets[i].setX(int(posX + widget_offsets[i][0]*cell_size))
      widgets[i].setY(int(posY + widget_offsets[i][1]*cell_size))
    for i in range(len(p_widgets)):
      p_widgets[i][0] = posX-cell_size * p_widget_offsets[i][0]
      p_widgets[i][1] = posY-cell_size * p_widget_offsets[i][1]

  else:
    button.setY(posY)
    for i in range(len(c_widgets)):
      c_widgets[i].move_ip(-cell_size*c_widget_offsets[i][0], -cell_size*c_widget_offsets[i][1])
    for i in range(len(widgets)):
      widgets[i].setX(int(posX - offset[0]*cell_size+ widget_offsets[i][0]*cell_size))
      widgets[i].setY(int(posY - offset[1]*cell_size+ widget_offsets[i][1]*cell_size))

    for i in range(len(p_widgets)):
      p_widgets[i][0] = posX- offset[0]*cell_size+cell_size*p_widget_offsets[i][0]
      p_widgets[i][1] = posY- offset[1]*cell_size+cell_size*p_widget_offsets[i][1]

    


wind_button_pos = [(14.5)*cell_size + cell_gap/2, (0)*cell_size]
wind_button = Button(
    screen,
    wind_button_pos[0],wind_button_pos[1],
    (1)*cell_size-cell_gap, (0.4)*cell_size-cell_gap,

    text='WIND', fontSize=16,textVAlign="centre",
    inactiveColour=(250, 250, 255), hoverColour=(200, 200, 200),
    pressedColour=(50, 50, 50), radius=10,
    onClick=lambda: widget_on_off_Y(wind_button,wind_button_pos[0],wind_button_pos[1],[0,1.5],
                                    [wind_widget],
                                    [[0,2]],
                                    [wind_slider,wind_output,wind_dir_output],
                                    [[0.9,0.25],[0.85,0.5],[0.85,0.95]],
                                    [wind_dir_pos],
                                    [[-0.1,-0.75]])
)
wind_slider = Slider(screen, 100, -100, 35, 10, min=10, max=20, step=1)
wind_output = Button(screen, 475, -200, 45, 30, fontSize=15,radius=5)
wind_output.disable()  # Act as label instead of textbox

wind_dir_output = Button(screen, 475, -200, 45, 30, fontSize=15,radius=5)
wind_dir_output.disable()  # Act as label instead of textbox


wind_dir_back=pg.image.load("../IMG/wind_dir_back.png")
wind_dir_back.convert()
wind_dir_arrow=pg.image.load("../IMG/wind_dir_arrow_2.png")
wind_dir_arrow.convert()
water_dir_back=pg.image.load("../IMG/water_dir_back.png")
water_dir_back.convert()
water_dir=pg.image.load("../IMG/water_dir.png")
water_dir.convert()

wind_dir_pos=[-300,-300]
wind_dir_size=0.2
wind_angle=0

pre_wind_angle=0
interp_wind_angle=0
interp_time=0
interp_duration=10

wind_widget=pg.Rect((14)*cell_size+cell_gap/2, (-2)*cell_size+cell_gap/2,(2)*cell_size-cell_gap, (1.5)*cell_size-cell_gap)


mouse = pg.mouse.get_pos()

run=True

playerBoatImg=pg.image.load("../IMG/player_boat.png")
playerBoatImg.convert()

aiBoatImg=pg.image.load("../IMG/ai_boat.png")
aiBoatImg.convert()

boatSize = 65
fps = 40

startAngle = r.randrange(0,359)

Player_boat=boat([window_size[0]/2,window_size[1]/2],startAngle)
AI_boat=boat([window_size[0]/2,window_size[1]/2],startAngle)

Player_boat.setColor([200,250,200])
AI_boat.setColor([250,200,250])

Player_boat.setSize(boatSize)
AI_boat.setSize(boatSize)

Player_boat.setImg(playerBoatImg)
AI_boat.setImg(aiBoatImg)

Player_boat.setFPS(fps)
AI_boat.setFPS(fps)

wind_angles=[0,5,10,15,20,25,32,36,40,45,52,60,70,80,90,100,110,120,130,140,150,160,170,180]
speeds=[0.0,0.5,1.1,1.4,1.9,2.4,3.7,4.3,4.8,5.2,5.8,6.2,6.4,6.6,6.8,6.8,6.7,6.4,5.8,5.2,4.6,4.0,3.6,3.4]

Player_boat.setsSailData(wind_angles,speeds)
AI_boat.setsSailData(wind_angles,speeds)

Player_boat.setWindowSize(window_size)
AI_boat.setWindowSize(window_size)

Player_boat.setPointsSettings(180,270,90,5)
AI_boat.setPointsSettings(180,270,90,5)
track =[[8,4.5],[9.4,2.1],[12.6,2.1],
        [13.5,4.3],[11,5.5],[13.5,6.6],
        [6.8,7],[5.3,4.4],[3.1,4.8],
        [5.2,6.1],[2.3,6.9],[2.1,2.2]]

for i in range(len(track)):
  track[i][0]*=cell_size
  track[i][1]*=cell_size

Player_boat.setPoints(track)
AI_boat.setPoints(track)

turnStrength = 10
maxTurnVel = 175

Player_boat.setMaxAngleVel(maxTurnVel)
AI_boat.setMaxAngleVel(maxTurnVel)

Player_boat.setTurnStrength(turnStrength)
AI_boat.setTurnStrength(turnStrength)

Player_boat.setSidewaysGrip(10)
AI_boat.setSidewaysGrip(10)

Player_boat.setSpeedScala(2)
AI_boat.setSpeedScala(2)

Player_boat.setSailAccStrength(0.75)
AI_boat.setSailAccStrength(0.75)

Player_boat.setWind(10,270)
AI_boat.setWind(10,270)


import torch
import torch.nn as nn
import torch.nn.functional as F

n_observations = AI_boat.getObs().size
n_actions = 3

# if GPU is to be used
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

class DQN(nn.Module):

  def __init__(self, n_observations, n_actions):
    super(DQN, self).__init__()
    self.layer1 = nn.Linear(n_observations, 128)
    self.layer2 = nn.Linear(128, 128)
    self.layer3 = nn.Linear(128, n_actions)

  # Called with either one element to determine next action, or a batch
  # during optimization. Returns tensor([[left0exp,right0exp]...]).
  def forward(self, x):
    x = F.relu(self.layer1(x))
    x = F.relu(self.layer2(x))
    return self.layer3(x)
  

policy_net = DQN(n_observations, n_actions).to(device)
policy_net.load_state_dict(torch.load("../AI/SailBoat_AI_S.pth", map_location=device))


class wind:
  def __init__(self,length,offset,window_size):
    self.t = 0
    self.l = length
    self.window_size=window_size
    self.pos=[offset[0],offset[1]]

  def run_wind(self,wind_speed,wind_angle):
    self.pos[0] += math.sin(math.radians(wind_angle))*wind_speed
    self.pos[1] += -math.cos(math.radians(wind_angle))*wind_speed
    self.pos = [self.pos[0]%self.window_size[0],self.pos[1]%self.window_size[1]]
    s = pg.Surface((3,3), pg.SRCALPHA)
    pg.draw.circle(s, (255,255,255,50), (1.5,1.5), 1.5)
    self.t += wind_speed
    for x in range(int(self.l)):
      
      w_pos=self.pos.copy()
      w_pos[0]+=math.sin(math.radians(wind_angle))*x + math.cos((x+self.t) * 0.2)
      w_pos[1]+=-math.cos(math.radians(wind_angle))*x + math.sin((x+self.t) * 0.2)
      screen.blit(s, w_pos)


wind_total=50
wind_list=[]

for w in range(wind_total):
  wind_list.append(wind(r.uniform(20,25),
                        [r.uniform(-cell_size*width_aspect/4*3,cell_size*width_aspect/4*3),
                         r.uniform(-cell_size*heigth_aspect/4*3,cell_size*heigth_aspect/4*3)],
                         window_size))


while run:
  events = pg.event.get()
  key= pg.key.get_pressed()


  if key[pg.K_r]:
    rAngle=r.randrange(0,359)
    
    Player_boat.reset([window_size[0]/2,window_size[1]/2],rAngle,wind_slider.getValue(),wind_angle)
    AI_boat.reset([window_size[0]/2,window_size[1]/2],rAngle,wind_slider.getValue(),wind_angle)
    Player_boat.setPoints(track)
    AI_boat.setPoints(track)
  else:
    Player_boat.setWind(wind_slider.getValue(),int(wind_angle-180)% 360)
    AI_boat.setWind(wind_slider.getValue(),int(wind_angle-180)% 360)
  
  AI_boat.getDirVectors()
  state_np = AI_boat.getObs()

  state = torch.tensor(state_np, dtype=torch.float32, device=device).unsqueeze(0)

  with torch.no_grad():
    action = policy_net(state).max(1).indices.item()

  if action == 0 and not key[pg.K_RIGHT]:
    AI_boat.turn(0)
  elif action == 1 and not key[pg.K_LEFT]:
    AI_boat.turn(1)
  else:
    AI_boat.turn(2)

  if key[pg.K_LEFT]:
    AI_boat.turn(0)
  if key[pg.K_RIGHT]:
    AI_boat.turn(1)

  if key[pg.K_a]:
    Player_boat.turn(0)
  elif key[pg.K_d]:
    Player_boat.turn(1)
  else:
    Player_boat.turn(2)

  if key[pg.K_w]:
    Player_boat.sail(False)
  else:
    Player_boat.sail()

  if key[pg.K_UP]:
    AI_boat.sail(False)
  else:
    AI_boat.sail()

  Player_boat.getDirVectors()
  AI_boat.getDirVectors()
  Player_boat.update()
  AI_boat.update()

  screen.fill((water_color))
  img = pg.transform.rotozoom(wind_dir_back, 0, wind_dir_size)
  img_arrow = pg.transform.rotozoom(wind_dir_arrow, -wind_angle, wind_dir_size)

  rect = img.get_rect()
  rect.center =wind_dir_pos

  rect_arrow = img_arrow.get_rect()
  rect_arrow.center = wind_dir_pos

  scale_factor = cell_size / water_dir_back.get_width()

  water_back_img=pg.transform.rotozoom(water_dir_back, 0, scale_factor)
  water_back_rect = water_back_img.get_rect()

  water_img=pg.transform.rotozoom(water_dir, -interp_wind_angle, scale_factor)
  water_rect = water_img.get_rect()

  tint_color = (130, 190, 255)

  tinted_water_back_img = water_back_img.copy()
  tinted_water_back_img.fill(tint_color, special_flags=pg.BLEND_RGB_MULT)

  tinted_water_img = water_img.copy()
  tinted_water_img.fill(tint_color, special_flags=pg.BLEND_RGB_MULT)
  for i in range(width_aspect):
    for j in range(heigth_aspect):
      
      water_back_rect.topleft =[i*cell_size,j*cell_size]
      
      water_rect.center =[i*cell_size+cell_size/2,j*cell_size+cell_size/2]

      screen.blit(tinted_water_back_img, water_back_rect)
      
      screen.blit(tinted_water_img, water_rect)
  
  for w in range(wind_total):
    wind_list[w].run_wind(wind_slider.getValue(),interp_wind_angle)


  for event in events:
    if event.type==pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
      mouse = event.pos
      x = mouse[0] - wind_dir_pos[0]
      y = mouse[1] - wind_dir_pos[1]
      pre_wind_angle = interp_wind_angle
      interp_time = 0
      wind_angle = math.degrees(math.atan2(x,-y))% 360

  def easeOutQuart(x):
    return 1 - (1 - x)**4

  interp_time+=1/interp_duration
  interp_wind_angle = pre_wind_angle + ((wind_angle - pre_wind_angle+180)%360-180)*easeOutQuart(min(1,interp_time))
  interp_wind_angle %= 360
  pg.draw.rect(screen, (255,255,255), wind_widget,border_radius=10)

  screen.blit(img, rect)
  #pg.draw.rect(screen, "RED", rect, 1)
  screen.blit(img_arrow, rect_arrow)
  #pg.draw.rect(screen, "RED", rect_arrow, 1)

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  Player_boat.show(90,screen)
  AI_boat.show(90,screen)

  AI_boat.getTargetPoint(40,False)
  Player_boat.getTargetPoint(40,False)
  
  Player_boat.drawPoints(screen,font,[255,255,255],25,[200,50,50])
  AI_boat.drawPoints(screen,font,[255,255,255],20,[250,50,50])

  wind_output.setText(str(int(wind_slider.getValue()))+" kn")
  wind_dir_output.setText(str(int(wind_angle-180)% 360)+"°")

  pg_w.update(events)  # Call once every loop to allow widgets to render and listen
  pg.display.update()

  

pg.quit()