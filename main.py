#!/usr/bin/env python3

import os
import random

import pyglet
# slow version: 2.0.14
# fast version: 1.5.27
from pyglet.gl import *

from Game import *
from Team import *
from Tile import *
from Ball import *

# The window is 31 x 29 tiles
idealDims = (256, 240)
Window = pyglet.window.Window(fullscreen=True)
Window.set_mouse_visible(False)
glEnable(GL_BLEND)
realDims = Window.get_size()
x = realDims[0]/idealDims[0]
y = realDims[1]/idealDims[1]
scale = min(x, y)
glScalef(scale, scale, 1)
Blinders = []
if scale == x:
  # untested
  h = realDims[1]/scale-idealDims[1]
  Blinders.append(pyglet.shapes.Rectangle(0, -h, idealDims[0], h, color=(0,0,0)))
  Blinders.append(pyglet.shapes.Rectangle(0, idealDims[1], idealDims[0], h, color=(0,0,0)))
  glTranslatef(0, (realDims[1]-(idealDims[1]*scale))/(2*scale), 0)
else:
  w = realDims[0]/scale-idealDims[0]
  Blinders.append(pyglet.shapes.Rectangle(-w, 0, w, idealDims[1], color=(0,0,0)))
  Blinders.append(pyglet.shapes.Rectangle(idealDims[0], 0, w, idealDims[1], color=(0,0,0)))
  glTranslatef((realDims[0]-(idealDims[0]*scale))/(2*scale), 0, 0)
# pyglet.options["vsync"] = None

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
HOME_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "HomeSprites.png"))
TILE_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "TileSprites.png"))
BALL_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "BallSprites.png"))
LOGO_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "LogoSprites.png"))
CHAR_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "CharSprites.png"))
SOUNDS = {
  "boom": pyglet.media.load(os.path.join(ASSETS, "boom.wav")),
  "explosion": pyglet.media.load(os.path.join(ASSETS, "explosion.wav")),
  "fanfare": pyglet.media.load(os.path.join(ASSETS, "fanfare.wav")),
  "hiss": pyglet.media.load(os.path.join(ASSETS, "hiss.wav")),
  "hit": pyglet.media.load(os.path.join(ASSETS, "hit.wav")),
  "slide": pyglet.media.load(os.path.join(ASSETS, "slide.wav")),
  "triangle": pyglet.media.load(os.path.join(ASSETS, "triangle.wav"))
}

TheGame = Game(TILE_SPRITE_SHEET, HOME_SPRITE_SHEET, BALL_SPRITE_SHEET, LOGO_SPRITE_SHEET, CHAR_SPRITE_SHEET, SOUNDS)

joysticks = pyglet.input.get_joysticks()
# for i,joystick in enumerate(joysticks[:2]):
#   joystick.open()
#   print(dir(joystick))
#   TheGame.teams[i*2].setInterface((lambda:joystick.x, lambda:False))
#   TheGame.teams[i*2+1].setInterface((lambda:joystick.z, lambda:False))
if len(joysticks) >= 1:
  joysticks[0].open()
  TheGame.teams[0].joystick = joysticks[0]
  TheGame.teams[1].joystick = joysticks[0]
if len(joysticks) >= 2:
  joysticks[1].open()
  TheGame.teams[2].joystick = joysticks[1]
  TheGame.teams[3].joystick = joysticks[1]

@Window.event
def on_draw():
  global TheGame, Blinders
  Window.clear()
  TheGame.blit()
  for rect in Blinders:
    rect.draw()

pyglet.clock.schedule(TheGame.step)
pyglet.app.run()
