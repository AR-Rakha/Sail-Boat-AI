import pygame as pg

import random as r
from Boat_Class import boat


pg.init()


width_aspect=16
heigth_aspect=9

cell_size=90
window_size=[cell_size*width_aspect,cell_size*heigth_aspect]

water_color=[140, 200, 255]

screen = pg.display.set_mode(window_size,pg.SHOWN)
pg.display.set_caption("Sail Boat Simulation Test")

ai_boat_img=pg.image.load("IMG/ai_boat.png")
ai_boat_img.convert()


AI_boat=boat([window_size[0]/2,window_size[1]/2],r.randrange(0,359))
AI_boat.setColor([200,200,200])
AI_boat.setSize(65)
AI_boat.setImg(ai_boat_img)
AI_boat.setFPS(100)

wind_angles=[0,5,10,15,20,25,32,36,40,45,52,60,70,80,90,100,110,120,130,140,150,160,170,180]
speeds=[0.0, 0.5, 1.1, 1.4, 1.9, 2.4, 3.7, 4.3, 4.8, 5.2, 5.8, 6.2, 6.4, 6.6, 6.8, 6.8, 6.7, 6.4, 5.8, 5.2, 4.6, 4.0, 3.6, 3.4]

AI_boat.setsSailData(wind_angles,speeds)
AI_boat.setWindowSize(window_size)

run=True

font = pg.font.SysFont('mono', 20,True,False)

AI_boat.setPointsSettings(180,270,90,5)
track =[[8,4.5],[9.4,2.1],[12.6,2.1],
        [13.5,4.3],[11,5.5],[13.5,6.6],
        [6.8,7],[5.3,4.4],[3.1,4.8],
        [5.2,6.1],[2.3,6.9],[2.1,2.2]]

for i in range(len(track)):
  track[i][0]*=cell_size
  track[i][1]*=cell_size
AI_boat.setPoints(track)

turnStrength = 10
maxTurnVel = 175

AI_boat.setMaxAngleVel(maxTurnVel)
AI_boat.setTurnStrength(turnStrength)
AI_boat.setSidewaysGrip(10)
AI_boat.setSpeedScala(2)
AI_boat.setSailAccStrength(0.75)
#AI_boat.setPointReward(10000)
#AI_boat.setLimit(window_size)
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
policy_net.load_state_dict(torch.load("AI/SailBoat_AI_S.pth", map_location=device))


while run:
  events = pg.event.get()
  screen.fill((water_color))

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  if key[pg.K_r]:
    AI_boat.reset([window_size[0]/2,window_size[1]/2],r.randrange(0,359),r.randrange(10,20,5),r.randrange(0,359))

  AI_boat.getDirVectors()
  state_np = AI_boat.getObs()

  state = torch.tensor(state_np, dtype=torch.float32, device=device).unsqueeze(0)


  with torch.no_grad():
    action = policy_net(state).max(1).indices.item()

  if action == 0:
    AI_boat.turn(0)
  elif action == 1:
    AI_boat.turn(1)
  else:
    AI_boat.turn(2)



  if key[pg.K_w]:
    AI_boat.sail(False)
  else:
    AI_boat.sail()

  AI_boat.getDirVectors()
  AI_boat.update()

  for event in events:
    if event.type==pg.QUIT:
      run = False

  AI_boat.show(90,screen)
  AI_boat.getTargetPoint(40,True)
  
  AI_boat.drawPoints(screen,font,[150,150,150],30,[50,50,150])

  pg.display.update()

pg.quit()