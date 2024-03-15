#!/usr/bin/env python3

import os
import random

import pyglet
# slow version: 2.0.14
# fast version: 1.5.27

from Team import *
from Sprite import *
from Game import *

pyglet.options["vsync"] = None
Window = pyglet.window.Window(256, 240)
# The window is 31 x 29
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
TILE_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "TileSprites.png"))
HOME_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "HomeSprites.png"))
B_A_L_L = pyglet.image.load(os.path.join(ASSETS, "B A L L.png"))

TheGame = Game(TILE_SPRITE_SHEET, HOME_SPRITE_SHEET)

joysticks = pyglet.input.get_joysticks()
joystick = joysticks[0]
joystick.open()
TheGame.teams[0].setInterface((lambda:joystick.x, lambda:False), HOME_SPRITE_SHEET)

@Window.event
def on_draw():
  global TheGame
  Window.clear()
  TheGame.blit(B_A_L_L)

# def newGame():
#   global TheGame
#   TheGame.step()

pyglet.clock.schedule(TheGame.step)
pyglet.app.run()
