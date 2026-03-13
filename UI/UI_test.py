import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

import math

pg.init()

width_aspect=16
heigth_aspect=9

cell_size=90
cell_gap=10

water_color=[140, 200, 255]

screen = pg.display.set_mode((cell_size*width_aspect,cell_size*heigth_aspect),pg.SHOWN)
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

    


wind_button_pos = [(14.5)*cell_size + cell_gap/2, (-0.25)*cell_size + cell_gap/2]
wind_button = Button(
    screen,
    wind_button_pos[0],wind_button_pos[1],
    (1)*cell_size-cell_gap, (0.5)*cell_size-cell_gap,

    text='WIND', fontSize=16,textVAlign="top",
    inactiveColour=(250, 250, 255), hoverColour=(200, 200, 200),
    pressedColour=(0, 200, 20), radius=10,
    onClick=lambda: widget_on_off_Y(wind_button,wind_button_pos[0],wind_button_pos[1],[0,1.5],
                                    [wind_widget],
                                    [[0,2],[0,2]],
                                    [wind_slider,wind_output,wind_dir_output],
                                    [[0.9,0.5],[0.85,0.75],[0.85,1.2]],
                                    [wind_dir_pos],
                                    [[-0.1,-0.9]])
)
wind_slider = Slider(screen, 100, -100, 28, 10, min=1, max=5, step=0.5)
wind_output = Button(screen, 475, -200, 45, 30, fontSize=15,radius=5)
wind_output.disable()  # Act as label instead of textbox

wind_dir_output = Button(screen, 475, -200, 45, 30, fontSize=15,radius=5)
wind_dir_output.disable()  # Act as label instead of textbox

wind_dir_pos=[300,300]
wind_dir_back=pg.image.load("IMG/wind_dir_back.png")
wind_dir_back.convert()
wind_dir_arrow=pg.image.load("IMG/wind_dir_arrow_2.png")
wind_dir_arrow.convert()
wind_dir_size=0.2
wind_dir_angle=0

wind_widget=pg.Rect((14)*cell_size+cell_gap/2, (-2)*cell_size+cell_gap/2,(2)*cell_size-cell_gap, (1.5)*cell_size-cell_gap)


mouse = pg.mouse.get_pos()

run=True

while run:
  events = pg.event.get()
  screen.fill((water_color))
  img = pg.transform.rotozoom(wind_dir_back, 0, wind_dir_size)
  img_arrow = pg.transform.rotozoom(wind_dir_arrow, wind_dir_angle, wind_dir_size)
  rect = img.get_rect()
  rect.center =wind_dir_pos
  rect_arrow = img_arrow.get_rect()
  rect_arrow.center = wind_dir_pos
  
  for event in events:
    if event.type==pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
      mouse = event.pos
      x = mouse[0] - wind_dir_pos[0]
      y = mouse[1] - wind_dir_pos[1]

      wind_dir_angle = math.degrees(-math.atan2(y, x))-90
  
  pg.draw.rect(screen, (255,255,255), wind_widget,border_radius=10)

  screen.blit(img, rect)
  pg.draw.rect(screen, "RED", rect, 1)
  screen.blit(img_arrow, rect_arrow)
  pg.draw.rect(screen, "RED", rect_arrow, 1)

  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False

  wind_output.setText(str(float(wind_slider.getValue()))+" m/s")
  pg_w.update(events)  # Call once every loop to allow widgets to render and listen
  pg.display.update()

  

pg.quit()