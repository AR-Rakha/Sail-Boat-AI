import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pg.init()

width_aspect=16
heigth_aspect=9

cell_size=90
cell_gap=10

water_color=[140, 200, 255]

screen = pg.display.set_mode((cell_size*width_aspect,cell_size*heigth_aspect),pg.SHOWN)
pg.display.set_caption("Sail Boat Test UI")

def widget_on_off_Y(button,posX,posY,offset,border,border_offset,widget1,widget1_offset,widget2,widget2_offset):
  button.on = not getattr(button, "on", False)

  if button.on:
    button.setY(posY + offset[1]*cell_size)
    border.move_ip(cell_size*border_offset[0], cell_size*border_offset[1])
    widget1.setX(int(posX + widget1_offset[0]*cell_size))
    widget1.setY(int(posY + widget1_offset[1]*cell_size))
    widget2.setX(int(posX + widget2_offset[0]*cell_size))
    widget2.setY(int(posY + widget2_offset[1]*cell_size))
  else:
    button.setY(posY)
    border.move_ip(-cell_size*border_offset[0], -cell_size*border_offset[1])
    widget1.setX(int(posX - offset[0]*cell_size+ widget1_offset[0]*cell_size))
    widget1.setY(int(posY - offset[1]*cell_size+ widget1_offset[1]*cell_size))
    widget2.setX(int(posX - offset[0]*cell_size+ widget2_offset[0]*cell_size))
    widget2.setY(int(posY - offset[1]*cell_size+ widget2_offset[1]*cell_size))
    


wind_button_pos = [(14.5)*cell_size + cell_gap/2, (-0.25)*cell_size + cell_gap/2]
wind_button = Button(
    screen,
    wind_button_pos[0],wind_button_pos[1],
    (1)*cell_size-cell_gap, (0.5)*cell_size-cell_gap,

    text='WIND', fontSize=16,textVAlign="top",
    inactiveColour=(250, 250, 255), hoverColour=(200, 200, 200),
    pressedColour=(0, 200, 20), radius=10,
    onClick=lambda: widget_on_off_Y(wind_button,wind_button_pos[0],wind_button_pos[1],[0,1.5],wind_widget,[0,2],wind_slider,[0.9,0.5],wind_output,[0.85,1])
)
wind_slider = Slider(screen, 100, -100, 28, 10, min=1, max=5, step=0.5)
wind_output = TextBox(screen, 475, -200, 40, 28, fontSize=15)
wind_output.disable()  # Act as label instead of textbox

wind_widget=pg.Rect((14)*cell_size+cell_gap/2, (-2)*cell_size+cell_gap/2,(2)*cell_size-cell_gap, (1.5)*cell_size-cell_gap)



run=True

while run:
  events = pg.event.get()
  screen.fill((water_color))
  
  pg.draw.rect(screen, (255,255,255), wind_widget,border_radius=10)


  key= pg.key.get_pressed()

  if key[pg.K_ESCAPE]:
    run = False
  
  for event in events:
    if event.type==pg.QUIT:
      run = False

  wind_output.setText(wind_slider.getValue())
  pg_w.update(events)  # Call once every loop to allow widgets to render and listen
  pg.display.update()

  

pg.quit()