import math
import numpy as np
from scipy.interpolate import interp1d
import pygame as pg
import random as r

def dot(v1=[0,1],v2=[1,0]):
  return v1[0]*v2[0]+v1[1]*v2[1]

class boat:
  def __init__(self,pos,angle,size,color):
    self.pos=pos
    self.vel=[0,0]
    self.acc=[0,0]

    self.angle = angle
    self.angle_vel=0
    self.angle_acc=0

    self.maxAngleVel=100

    self.turnStrength = 1
    self.sidewaysGrip = 1
    self.windSpeed = 0
    self.windAngle = 0
    self.sailAccelerationStrength=1
    

    self.size = size
    self.limit = [100,100]

    self.boat = None
    self.boat_rect = None

    self.scale_factor=1
    
    self.color=color

    self.wind_angles=[]
    self.speeds_line=[]

    self.f_speed = 0

    self.points=[]
    self.targetIndex=0

    self.targetV=[]
    self.nextV=[]

    self.forwardV=[math.cos(self.angle),math.sin(self.angle)]
    self.rigthV=[math.sin(self.angle),math.cos(self.angle)]
    self.windV=[]

    self.windDirX = 0
    self.windDirY = 0
    self.targetDirY = 0
    self.targetDirX = 0
    self.nextDirY = 0
    self.nextDirX = 0 


    self.fps=400
    self.dt = 1/self.fps

    self.timeLimit=0 # seconds
    self.time=0

    self.reward=0
    self.tsReward=0 # reward this TimeStep (ts)

    self.pointReward = 1
    self.pointReached = False
    
  def setsSailData(self,angles,speeds):
    self.wind_angles=angles
    self.speeds_line=speeds

    self.f_speed = interp1d(self.wind_angles, self.speeds_line, kind='cubic')

  def setFPS(self,fps=400):
    self.fps=fps
    self.dt = 1/self.fps

  def setImg(self,img):
    self.scale_factor = self.size / img.get_width()
    self.boat = img

  def setMaxAngleVel(self,max_angle_vel):
    self.maxAngleVel=max_angle_vel

  def setTurnStrength(self,turn_strength):
    self.turnStrength =turn_strength

  def setSidewaysGrip(self,sidewaysGrip):
    self.sidewaysGrip = sidewaysGrip
  def setSpeedScala(self,scala):
    self.speedScala=scala

  def setWind(self,wind_speed,wind_angle):
    self.windSpeed = wind_speed
    self.windAngle = wind_angle

  def setSailAccStrength(self,strength):
    self.sailAccelerationStrength = strength

  def setPointReward(self,reward):
    self.pointReward = reward

  def setLimit(self,limit):
    self.limit = limit

  def show(self,angleOffset,screen):
    boat_img = pg.transform.rotozoom(self.boat, (-self.angle+angleOffset), self.scale_factor)
    self.boat_rect = boat_img.get_rect()
    self.boat_rect.center = self.pos
    tinted_boat = boat_img.copy()
    tinted_boat.fill(self.color, special_flags=pg.BLEND_RGB_MULT)
    screen.blit(tinted_boat, self.boat_rect)
  
  def turn(self,turnDir):
    if turnDir == 0:
      self.angle_acc =  (self.maxAngleVel - abs(self.angle_vel))*-self.turnStrength
    else:
      self.angle_acc =  (self.maxAngleVel - abs(self.angle_vel))*self.turnStrength

  def sail(self,wind=True):
    
    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))

    forward_speed = self.vel[0]*fx + self.vel[1]*fy

    if wind:
      speed_error = self.getBoatSpeed() - forward_speed
    else:
      speed_error = 0 - forward_speed

    
    self.acc[0] += fx * speed_error * self.sailAccelerationStrength
    self.acc[1] += fy * speed_error * self.sailAccelerationStrength

    #print(speed_error)


  def getBoatSpeed(self):
    return self.f_speed(self.rel_angle(self.windAngle,self.angle))*self.windSpeed*self.speedScala

  def rel_angle(self,wind_angle,boat_angle):
    delta = (wind_angle - boat_angle) % 360
    return delta if delta <= 180 else 360 - delta

  def update(self):
    # rotation
    self.angle_vel *= 0.99
    self.angle_vel += self.angle_acc * self.dt
    self.angle += self.angle_vel * self.dt

    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))
    sx = -fy
    sy = fx

    # remove sideways drift
    sideways_speed = self.vel[0]*sx + self.vel[1]*sy
    
    self.acc[0] -= sx * sideways_speed * self.sidewaysGrip
    self.acc[1] -= sy * sideways_speed * self.sidewaysGrip

    # apply acceleration to velocity
    self.vel[0] += self.acc[0] * self.dt
    self.vel[1] += self.acc[1] * self.dt

    # --- now move ---
    self.pos[0] += self.vel[0] * self.dt
    self.pos[1] += self.vel[1] * self.dt

    # reset
    self.angle_acc = 0
    self.acc = [0,0]

    self.forwardV=[math.sin(math.radians(self.angle)),-math.cos(math.radians(self.angle))]
    self.rigthV=[math.cos(math.radians(self.angle)),-math.sin(math.radians(self.angle))]

  def generatePoints(self,window_size,borderOffset,num=10,minDist=90):
    self.targetIndex=0
    self.points=[[r.randrange(0+borderOffset,window_size[0]-borderOffset),r.randrange(0+borderOffset,window_size[1]-borderOffset)]]
    for x in range(num-1):
      toClose=True
      randP=[r.randrange(0+borderOffset,window_size[0]-borderOffset),r.randrange(0+borderOffset,window_size[1]-borderOffset)]

      while toClose:
        toClose=False
        randP=[r.randrange(0+borderOffset,window_size[0]-borderOffset),r.randrange(0+borderOffset,window_size[1]-borderOffset)]
        for d in range(len(self.points)):
          if math.sqrt((self.points[d][0]-randP[0])**2+(self.points[d][1]-randP[1])**2)<minDist:
            toClose=True
            break

      self.points.append(randP.copy())
    
  def setTimeLimit(self,limitInSeconds):
    self.timeLimit=limitInSeconds

  def timeReset(self):
    if self.time/self.fps>=self.timeLimit:
      self.reset()
      self.resetReward()

  def reset(self,startangle=0, startPos=[0,0]):
    self.angle=startangle
    self.pos=startPos
    self.time=0
    self.resetReward()
    self.getDirVectors()

    obs = np.array([self.windDirY,
      self.windDirX,
      self.targetDirY,
      self.targetDirX,
      self.nextDirY,
      self.nextDirX], dtype=np.float32)

    return obs

  
  def addReward(self,preDist,dist):
    r = preDist - dist + int(self.pointReached)*self.pointReward
    self.reward+=r
    self.tsReward=r

    self.pointReached = False
  
  def addTime(self):
    self.time+=1

  def resetReward(self):
    self.reward=0

  def step(self,action):
    preDist = self.getDist()


    # 0 = left, 1 = right
    self.turn(action)
    self.sail()

    self.update()
    dist = self.getDist()

    self.getDirVectors()
    self.addTime()
    self.addReward(preDist,dist)

    terminated = (-self.limit[0]/2 > self.pos[0] or self.limit[0]/2*3 < self.pos[0] or -self.limit[1]/2 > self.pos[1] or self.limit[1]/2*3 < self.pos[1])
    truncated = self.time/self.fps >= self.timeLimit or self.targetIndex > len(self.points)

    # Observation
    obs = np.array([self.windDirY,
      self.windDirX,
      self.targetDirY,
      self.targetDirX,
      self.nextDirY,
      self.nextDirX], dtype=np.float32)

    
    reward = self.tsReward

    info = {}
    return obs, reward, terminated, truncated, info

  def getDist(self):
    dist = math.sqrt((self.points[self.targetIndex][0]-self.pos[0])**2+(self.points[self.targetIndex][1]-self.pos[1])**2)
    return dist

  def getTargetPoint(self,minDist,generateNewPoints=False):
    if self.targetIndex >= len(self.points) and not generateNewPoints:
      return False
    elif self.targetIndex >= len(self.points) and generateNewPoints:
      return True

    if self.getDist() < minDist:
      self.targetIndex += 1
      self.pointReached = True
    
  def drawPoints(self,screen,font):
    for x in range(len(self.points)-self.targetIndex):
      pg.draw.circle(screen, (0,0,0), (self.points[x+self.targetIndex][0],self.points[x+self.targetIndex][1]), 15)
      textImg = font.render(str(x+self.targetIndex+1), True, (255,255,255))
      text_width, text_height = font.size(str(x+self.targetIndex+1)) #txt being whatever str you're rendering
      screen.blit(textImg, (self.points[x+self.targetIndex][0]-text_width/2,self.points[x+self.targetIndex][1]-text_height/2))

  def getPoints(self):
    return self.points
  def setPoints(self,points):
    self.points = points

  def getDirVectors(self):
    self.windV=[-math.sin(math.radians(self.windAngle)),-math.cos(math.radians(self.windAngle))]


    self.windDirY = dot(self.forwardV,self.windV)
    self.windDirX = dot(self.rigthV,self.windV)

    targetV = [self.points[self.targetIndex][0]-self.pos[0],self.points[self.targetIndex][1]-self.pos[1]]
    nextV = []
    if self.targetIndex + 1 >= len(self.points):
      nextV = targetV
    else:
      nextV = [self.points[self.targetIndex+1][0]-self.pos[0],self.points[self.targetIndex+1][1]-self.pos[1]]

    self.targetDirY = dot(self.forwardV,targetV)
    self.targetDirX = dot(self.rigthV,targetV)
    self.nextDirY = dot(self.forwardV,nextV)
    self.nextDirX = dot(self.rigthV,nextV)
    


  



