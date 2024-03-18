#!/usr/bin/env python3

import os
import random

import pyglet
# slow version: 2.0.14
# fast version: 1.5.27

from Game import *
from Team import *
from Tile import *
from Ball import *

pyglet.options["vsync"] = None
Window = pyglet.window.Window(256, 240)
# The window is 31 x 29 tiles
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
HOME_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "HomeSprites.png"))
TILE_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "TileSprites.png"))
BALL_SPRITE_SHEET = pyglet.image.load(os.path.join(ASSETS, "B A L L.png"))

TheGame = Game(TILE_SPRITE_SHEET, HOME_SPRITE_SHEET, BALL_SPRITE_SHEET)

# joysticks = pyglet.input.get_joysticks()
# joystick = joysticks[0]
# joystick.open()
# TheGame.teams[0].setInterface((lambda:joystick.x, lambda:False), HOME_SPRITE_SHEET)

@Window.event
def on_draw():
  global TheGame
  Window.clear()
  TheGame.blit()

# def newGame():
#   global TheGame
#   TheGame.step()

pyglet.clock.schedule(TheGame.step)
pyglet.app.run()
