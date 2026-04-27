import math
import numpy as np
from scipy.interpolate import interp1d
import pygame as pg
import random as r

def lengthV(v=[0,1]):
  return math.sqrt(v[0]**2+v[1]**2)

def dot1(v1, v2, eps=1e-6):
  v1_length = lengthV(v1)
  v2_length = lengthV(v2)

  if v1_length < eps or v2_length < eps:
    return 0.0  # direction undefined → neutral signal

  v1_norm = [v1[0]/v1_length, v1[1]/v1_length]
  v2_norm = [v2[0]/v2_length, v2[1]/v2_length]

  return v1_norm[0]*v2_norm[0] + v1_norm[1]*v2_norm[1]

def dot2(v1, v2, eps=1e-6):
  v1_length = lengthV(v1)
  v2_length = lengthV(v2)

  if v1_length < eps or v2_length < eps:
    return 0.0  # direction undefined → neutral signal

  return v1[0]*v2[0] + v1[1]*v2[1]


class boat:
  def __init__(self,pos,angle):
    self.pos = pos
    self.vel = [0,0]
    self.acc = [0,0]

    self.angle = angle
    self.angle_vel = 0
    self.angle_acc = 0

    self.maxAngleVel = 100
    self.sailAccelerationStrength = 1

    self.turnStrength = 1
    self.sidewaysGrip = 1
    self.windSpeed = 0
    self.windAngle = 0

    self.size = 50
    self.limit = [100,100]
    self.windowSize=[0,0]

    self.boat = None
    self.boat_rect = None

    self.scale_factor = 1
    self.color = [0,0,0]

    self.wind_angles = []
    self.speeds_line = []

    self.f_speed = 0

    self.points = []
    self.targetIndex = 0

    self.targetV = []
    self.nextV = []

    self.forwardV = [math.cos(self.angle),math.sin(self.angle)]
    self.rightV = [math.sin(self.angle),math.cos(self.angle)]
    self.windV = []

    self.forwardSpeed = 0
    self.sidewaysSpeed = 0
    self.windDirX = 0
    self.windDirY = 0

    self.targetDirY = 0
    self.targetDirX = 0
    self.targetDirY_n = 0
    self.targetDirX_n = 0

    self.nextDirY = 0
    self.nextDirX = 0
    self.nextDirY_n = 0
    self.nextDirX_n = 0 

    self.speedTowardTarget = 0


    self.fps = 400
    self.dt = 1/self.fps

    self.timeLimit = 0 # seconds
    self.time = 0

    self.reward = 0
    self.tsReward = 0 # reward this TimeStep (ts)

    self.pointReward = 1
    self.pointReached = False

    self.minDist = 90
    self.maxDist = 180
    self.borderOffset = 90
    self.num = 10
    
  def setsSailData(self,angles,speeds):
    self.wind_angles = angles
    self.speeds_line = speeds

    self.f_speed = interp1d(self.wind_angles, self.speeds_line, kind='cubic')

  def setFPS(self,fps=400):
    self.fps = fps
    self.dt = 1/self.fps

  def setImg(self,img):
    self.scale_factor = self.size / img.get_width()
    self.boat = img

  def setMaxAngleVel(self,max_angle_vel):
    self.maxAngleVel = max_angle_vel

  def setTurnStrength(self,turn_strength):
    self.turnStrength = turn_strength

  def setSidewaysGrip(self,sidewaysGrip):
    self.sidewaysGrip = sidewaysGrip
  def setSpeedScala(self,scala):
    self.speedScala = scala

  def setWind(self,wind_speed,wind_angle):
    self.windSpeed = wind_speed
    self.windAngle = wind_angle

  def setSailAccStrength(self,strength):
    self.sailAccelerationStrength = strength

  def setPointReward(self,reward):
    self.pointReward = reward

  def setLimit(self,limit):
    self.limit = limit

  def setColor(self,color):
    self.color = color

  def setSize(self,size):
    self.size = size

  def setWindowSize(self,window_size):
    self.windowSize = window_size

  def setPointsSettings(self,minDist,maxDist,borderOffset=90,num=10):
    self.minDist = minDist
    self.maxDist = maxDist
    self.borderOffset = borderOffset
    self.num = num

  def show(self,angleOffset,screen):
    boat_img = pg.transform.rotozoom(self.boat, (-self.angle+angleOffset), self.scale_factor)
    self.boat_rect = boat_img.get_rect()
    self.boat_rect.center = self.pos
    tinted_boat = boat_img.copy()
    tinted_boat.fill(self.color, special_flags=pg.BLEND_RGB_MULT)
    screen.blit(tinted_boat, self.boat_rect)
  
  def turn(self,turnDir):
    if turnDir == 0:
      self.angle_acc = (self.maxAngleVel - abs(self.angle_vel)) *-self.turnStrength
    elif turnDir == 1:
      self.angle_acc = (self.maxAngleVel - abs(self.angle_vel)) * self.turnStrength
    else:
      self.angle_acc = 0

  def sail(self,wind=True):
    
    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))

    self.forwardSpeed = self.vel[0]*fx + self.vel[1]*fy

    if wind:
      speed_error = self.getBoatSpeed() - self.forwardSpeed
    else:
      speed_error = 0 - self.forwardSpeed

    
    self.acc[0] += fx * speed_error * self.sailAccelerationStrength
    self.acc[1] += fy * speed_error * self.sailAccelerationStrength

    #print(speed_error)


  def getBoatSpeed(self):
    return self.f_speed(self.rel_angle(self.windAngle,self.angle)) * self.windSpeed * self.speedScala

  def rel_angle(self,wind_angle,boat_angle):
    delta = (wind_angle - boat_angle) % 360
    return delta if delta <= 180 else 360 - delta

  def update(self):
    # rotation
    self.angle_vel *= 0.95
    self.angle_vel += self.angle_acc * self.dt
    self.angle_vel = max(-self.maxAngleVel, min(self.angle_vel, self.maxAngleVel))
    self.angle += self.angle_vel * self.dt
    self.angle = self.angle % 360

    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))
    sx = -fy
    sy = fx

    # remove sideways drift
    self.sidewaysSpeed = self.vel[0]*sx + self.vel[1]*sy
    
    self.acc[0] -= sx * self.sidewaysSpeed * self.sidewaysGrip
    self.acc[1] -= sy * self.sidewaysSpeed * self.sidewaysGrip

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
    self.rightV=[math.cos(math.radians(self.angle)),-math.sin(math.radians(self.angle))]

  def generatePoints(self):
    self.targetIndex=0
    self.points=[[self.windowSize[0]/2,self.windowSize[1]/2]]
    for x in range(self.num-1):
      outOfRange=True
      randR=r.randrange(0,359)
      randL=r.randrange(self.minDist,self.maxDist)
      randP=[self.points[x][0]+math.cos(math.radians(randR))*randL,self.points[x][1]+math.sin(math.radians(randR))*randL]

      while outOfRange:
        outOfRange=False
        randR=r.randrange(0,359)
        randL=r.randrange(self.minDist,self.maxDist)
        randP=[self.points[x][0]+math.cos(math.radians(randR))*randL,self.points[x][1]+math.sin(math.radians(randR))*randL]
        
        inBorderX = randP[0] > 0+self.borderOffset and randP[0] < self.windowSize[0]-self.borderOffset
        inBorderY = randP[1] > 0+self.borderOffset and randP[1] < self.windowSize[1]-self.borderOffset

        if not inBorderX or not inBorderY:
          outOfRange=True
        

      self.points.append(randP.copy())
    
  def setTimeLimit(self,limitInSeconds):
    self.timeLimit = limitInSeconds

  def timeReset(self):
    if self.time/self.fps >= self.timeLimit:
      self.reset()
      self.resetReward()

  def reset(self,startPos=[0,0],startangle=0,windSpeed=15,windAngle=0):
    self.targetIndex=0
    self.angle = startangle
    self.angle_vel = 0
    self.angle_acc = 0
    self.pos = startPos
    self.time = 0
    self.vel=[0,0]
    self.acc=[0,0]
    self.setWind(windSpeed,windAngle)
    self.resetReward()
    self.getDirVectors()
    self.generatePoints()

    obs = self.getObs()

    return obs

  
  def addReward(self,preDist,dist,terminated):
    r=0

    progress = preDist-dist

    #r -= abs(self.angle_vel)*0.001
    r += progress*0.1
    #r += self.speedTowardTarget * 0.5   
    r -= 0.01

    if self.pointReached:
      r += self.pointReward

    '''if terminated:
      r -= 50'''
      

    self.reward += r
    self.tsReward = r

    self.pointReached = False
  
  def addTime(self):
    self.time += 1

  def resetReward(self):
    self.reward = 0

  def step(self,action):
    preDist = self.getDist()

    # 0 = left, 1 = right, 2 = none
    self.turn(action)
    self.sail()

    self.update()
    self.getTargetPoint(15)
    dist = self.getDist()

    self.getDirVectors()
    self.addTime()

    terminated = (-90 > self.pos[0] or self.limit[0]+90 < self.pos[0] or -90 > self.pos[1] or self.limit[1]+90 < self.pos[1])
    truncated = self.time/self.fps >= self.timeLimit #or self.targetIndex > len(self.points)-1

    self.addReward(preDist,dist,terminated)

    # Observation
    obs = self.getObs()

    
    reward = self.tsReward

    info = {}
    return obs, reward, terminated, truncated, info

  def getDist(self):
    '''if self.targetIndex == len(self.points):
      dist = math.sqrt((self.points[self.targetIndex-1][0]-self.pos[0])**2+(self.points[self.targetIndex-1][1]-self.pos[1])**2)
    else:
      dist = math.sqrt((self.points[self.targetIndex][0]-self.pos[0])**2+(self.points[self.targetIndex][1]-self.pos[1])**2)'''
    
    dist = math.sqrt((self.points[self.targetIndex%(len(self.points))][0]-self.pos[0])**2+(self.points[self.targetIndex%(len(self.points))][1]-self.pos[1])**2)
    return dist

  def getTargetPoint(self,minDist,resetPoints=False):
    
    if self.targetIndex >= len(self.points):
      self.targetIndex=0
      if resetPoints:
        self.generatePoints()

    if self.getDist() < minDist:
      self.targetIndex += 1
      self.pointReached = True
    
  def drawPoints(self,screen,font,fontColor=[255,255,255],radius=15,color=[0,0,0]):
    for x in range(len(self.points)-self.targetIndex):
      pg.draw.circle(screen, color, (self.points[x+self.targetIndex][0],self.points[x+self.targetIndex][1]), radius)
      textImg = font.render(str(x+self.targetIndex+1), True, fontColor)
      text_width, text_height = font.size(str(x+self.targetIndex+1)) #txt being whatever str you're rendering
      screen.blit(textImg, (self.points[x+self.targetIndex][0]-text_width/2,self.points[x+self.targetIndex][1]-text_height/2))

  def getPoints(self):
    return self.points
  def setPoints(self,points):
    self.points = points

  def getDirVectors(self):

    fx = math.sin(math.radians(self.angle))
    fy = -math.cos(math.radians(self.angle))
    rx = math.cos(math.radians(self.angle))
    ry = -math.sin(math.radians(self.angle))

    self.forwardV = [fx, fy]
    self.rightV   = [rx, ry]

    self.windV = [-math.sin(math.radians(self.windAngle)),-math.cos(math.radians(self.windAngle))]


    self.windDirY = dot1(self.forwardV,self.windV)
    self.windDirX = dot1(self.rightV,self.windV)

    targetV = []
    nextV = []
    '''
    if self.targetIndex + 1 == len(self.points):
      targetV = [self.points[self.targetIndex][0] - self.pos[0],self.points[self.targetIndex][1] - self.pos[1]]
      nextV = targetV
    elif self.targetIndex + 1 > len(self.points):
      targetV = [0,0]
      nextV = targetV
    else:
      targetV = [self.points[self.targetIndex][0] - self.pos[0],self.points[self.targetIndex][1] - self.pos[1]]
      nextV = [self.points[self.targetIndex+1][0] - self.pos[0],self.points[self.targetIndex+1][1] - self.pos[1]]
  '''
    targetV = [self.points[self.targetIndex%(len(self.points))][0] - self.pos[0],self.points[self.targetIndex%(len(self.points))][1] - self.pos[1]]
    nextV = [self.points[(self.targetIndex+1)%(len(self.points))][0] - self.pos[0],self.points[(self.targetIndex+1)%(len(self.points))][1] - self.pos[1]]


    self.targetDirY = dot2(self.forwardV,targetV)
    self.targetDirX = dot2(self.rightV,targetV)
    self.targetDirY_n = dot1(self.forwardV,targetV)
    self.targetDirX_n = dot1(self.rightV,targetV)

    self.nextDirY = dot2(self.forwardV,nextV)
    self.nextDirX = dot2(self.rightV,nextV)
    self.nextDirY_n = dot1(self.forwardV,nextV)
    self.nextDirX_n = dot1(self.rightV,nextV)

    self.speedTowardTarget = self.targetDirY*self.forwardSpeed
    

  def getObs(self):

    dist = self.getDist()
    maxDist = math.sqrt(self.windowSize[0]**2 + self.windowSize[1]**2)
    distNorm = dist / maxDist

    obs = np.array([
      self.windDirY, self.windDirX,
      self.targetDirY,self.targetDirX,
      self.targetDirY_n,self.targetDirX_n,
      self.nextDirY,self.nextDirX,
      self.nextDirY_n,self.nextDirX_n,
      self.speedTowardTarget,
      self.angle_vel,
      distNorm], dtype=np.float32)

    '''self.nextDirY,self.nextDirX,distNorm'''

    return obs
  



