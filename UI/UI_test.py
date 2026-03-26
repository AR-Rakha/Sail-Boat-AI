import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

import math
import random

pg.init()

width_aspect=16
heigth_aspect=9

cell_size=90
cell_gap=10

window_size=[cell_size*width_aspect,cell_size*heigth_aspect]

water_color=[140, 200, 255]

screen = pg.display.set_mode(window_size,pg.SHOWN)
pg.display.set_caption("Sail Boat Test UI")

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
    pressedColour=(0, 200, 20), radius=10,
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


wind_dir_back=pg.image.load("IMG/wind_dir_back.png")
wind_dir_back.convert()
wind_dir_arrow=pg.image.load("IMG/wind_dir_arrow_2.png")
wind_dir_arrow.convert()
water_dir_back=pg.image.load("IMG/water_dir_back.png")
water_dir_back.convert()
water_dir=pg.image.load("IMG/water_dir.png")
water_dir.convert()

wind_dir_pos=[-300,-300]
wind_dir_size=0.2
wind_dir_angle=0

wind_widget=pg.Rect((14)*cell_size+cell_gap/2, (-2)*cell_size+cell_gap/2,(2)*cell_size-cell_gap, (1.5)*cell_size-cell_gap)


mouse = pg.mouse.get_pos()

run=True

t=0

class wind:
  def __init__(self,length,offset,window_size):
    self.t = 0
    self.l = length
    self.window_size=window_size
    self.pos=[0,0]
    self.offset=offset

  def run_wind(self,wind_speed,wind_angle):
    self.t -= wind_speed

    center_x = cell_size * width_aspect/2
    center_y = cell_size * heigth_aspect/2

    angle = math.radians(-wind_angle)

    for x in range(int(self.l)):
      self.pos = [center_x + math.sin(angle) * (x+self.t) + math.cos((x+self.t) * 0.2) - 1 + self.offset[0] ,
                center_y  + math.cos(angle) * (x+self.t) + math.sin((x+self.t) * 0.2)     + self.offset[1]]
      #(sin(a) t + cos(t * 0.5) - 1, cos(a) t + sin(t * 0.5))

      self.pos = [self.pos[0]%self.window_size[0],self.pos[1]%self.window_size[1]]

      pg.draw.circle(screen, (255,255,255), self.pos, 1)

wind_total=10
wind_list=[]

for w in range(wind_total):
  wind_list.append(wind(random.uniform(20,25),
                        [random.uniform(-cell_size*width_aspect/4*3,cell_size*width_aspect/4*3),
                         random.uniform(-cell_size*heigth_aspect/4*3,cell_size*heigth_aspect/4*3)],
                         window_size))


while run:
  events = pg.event.get()
  screen.fill((water_color))
  img = pg.transform.rotozoom(wind_dir_back, 0, wind_dir_size)
  img_arrow = pg.transform.rotozoom(wind_dir_arrow, -wind_dir_angle, wind_dir_size)
  rect = img.get_rect()
  rect.center =wind_dir_pos
  rect_arrow = img_arrow.get_rect()
  rect_arrow.center = wind_dir_pos
  
  for i in range(width_aspect):
    for j in range(heigth_aspect):
      scale_factor = cell_size / water_dir_back.get_width()
      water_back_img=pg.transform.rotozoom(water_dir_back, 0, scale_factor)
      water_back_rect = water_back_img.get_rect()
      water_back_rect.topleft =[i*cell_size,j*cell_size]
      water_img=pg.transform.rotozoom(water_dir, -wind_dir_angle, scale_factor)
      water_rect = water_img.get_rect()
      water_rect.center =[i*cell_size+cell_size/2,j*cell_size+cell_size/2]
      # Make a copy of your image first so you don't overwrite the original
      tinted_img = water_back_img.copy()
      # Example: tint with a light blue color
      tint_color = (130, 190, 255)  # RGB
      # Apply the tint
      tinted_img.fill(tint_color, special_flags=pg.BLEND_RGB_MULT)
      # Then blit as usual
      screen.blit(tinted_img, water_back_rect)
      # Make a copy of your image first so you don't overwrite the original
      tinted_img = water_img.copy()
      tint_color = (120, 180, 255)  # RGB
      # Apply the tint
      tinted_img.fill(tint_color, special_flags=pg.BLEND_RGB_MULT)
      # Then blit as usual
      screen.blit(tinted_img, water_rect)

  for w in range(wind_total):
    wind_list[w].run_wind(wind_slider.getValue(),wind_dir_angle)


  for event in events:
    if event.type==pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
      mouse = event.pos
      x = mouse[0] - wind_dir_pos[0]
      y = mouse[1] - wind_dir_pos[1]

      wind_dir_angle = math.degrees(math.atan2(x,-y))% 360
  
  pg.draw.rect(screen, (255,255,255), wind_widget,border_radius=10)

  screen.blit(img, rect)
  #pg.draw.rect(screen, "RED", rect, 1)
  screen.blit(img_arrow, rect_arrow)
  #pg.draw.rect(screen, "RED", rect_arrow, 1)

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  wind_output.setText(str(int(wind_slider.getValue()))+" kn")
  wind_dir_output.setText(str(int(wind_dir_angle-180)% 360)+"°")

  pg_w.update(events)  # Call once every loop to allow widgets to render and listen
  pg.display.update()

  

pg.quit()