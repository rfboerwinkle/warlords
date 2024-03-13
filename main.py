#!/usr/bin/env python3

import random

import pyglet

from Team import Team
from Sprites import *

Window = pyglet.window.Window(256, 240)
# The window is 31 x 29
TILE_SPRITE_SHEET = pyglet.image.load("assets/TileSprites.png")
HOME_SPRITE_SHEET = pyglet.image.load("assets/HomeSprites.png")
B_A_L_L = pyglet.image.load("assets/B A L L.png")

Tiles = populateTiles(TILE_SPRITE_SHEET)

Teams = [Team(i, TILE_SPRITE_SHEET, HOME_SPRITE_SHEET) for i in range(4)]
joysticks = pyglet.input.get_joysticks()
# print(joysticks)
joystick = joysticks[0]
joystick.open()
Teams[0].setInterface((lambda:joystick.x, lambda:False), HOME_SPRITE_SHEET)

BallX = 124
BallY = 116
# These are a little off because everything is lower-left based.
BalldX = 20
BalldY = 20
# pixels per second

@Window.event
def on_draw():
  global Tiles, Teams
  global B_A_L_L, BallX, BallY
  Window.clear()
  for tile in Tiles:
    tile.blit()
  for team in Teams:
    team.blit()
  B_A_L_L.blit(BallX, BallY, 0)

def physicsStep(dt):
  # dt is in seconds
  global Teams, Tiles
  global BallX, BallY, BalldX, BalldY

  BallX += BalldX*dt
  BallY += BalldY*dt

  if BallX < 0:
    BalldX *=-1
    BallX = 0
  elif BallX > 248:
    BalldX *= -1
    BallX = 248

  if BallY < 0:
    BalldY *=-1
    BallY = 0
  elif BallY > 232:
    BalldY *= -1
    BallY = 232

  for team in Teams:
    team.step()
    dx,dy = team.getShield()
    dx = abs(dx - BallX)
    dy = abs(dy - BallY)
    if dx <= 8 and dy <= 8:
      if dx<dy:
        BalldY *= -1
      else:
        BalldX *= -1
      break

  possibleTiles = []
  for i in range(len(Tiles)):
    dx = abs(Tiles[i].x-BallX)
    dy = abs(Tiles[i].y-BallY)
    if dx <= 8 and dy <= 8:
      possibleTiles.append((i, dx<dy))
  if possibleTiles:
    i = random.randrange(0,len(possibleTiles))
    Tiles.pop(possibleTiles[i][0])
    if possibleTiles[i][1]:
      BalldY *= -1
    else:
      BalldX *= -1

pyglet.clock.schedule(physicsStep)
pyglet.app.run()
