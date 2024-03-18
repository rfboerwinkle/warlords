import pyglet

from Team import *
from Tile import *
from Ball import *

class Game:
  def __init__(self, tileSprites, homeSprites, ballSprites, demo=False):
    self.tileSprites = tileSprites
    self.homeSprites = homeSprites
    self.ballSprites = ballSprites
    self.teams = []
    self.tiles = []
    self.balls = []

    self.reset()

    if demo:
      pass
    else:
      pass

  def reset(self):
    self.populateTeams()
    self.populateTiles()
    self.balls = []

  def step(self, dt):
    for team in self.teams:
      team.step(dt)
    for ball in self.balls:
      ball.step(dt)

  # ball argument is temp
  def blit(self):
    for tile in self.tiles:
      tile.blit()
    for team in self.teams:
      team.blit()
    for ball in self.balls:
      ball.blit()

  def populateTiles(self):
    tileList = (
      ((7,0), (6,0), (7,1), (6,1), (7,2), (6,2), (7,3), (6,3), (7,4), (6,4), (7,5), (6,5), (7,6), (6,6), (7,7), (6,7), (5,7), (5,6), (4,7), (4,6), (3,7), (3,6), (2,7), (2,6), (1,7), (1,6), (0,7), (0,6)),
      ((0,8), (3,8), (6,8)),
      ((1,8), (4,8), (7,8)),
      ((0,9), (1,9), (2,8), (3,9), (4,9), (5,8), (6,9), (7,9)),
      ((8,0), (8,3), (8,6)),
      ((8,1), (8,4), (8,7)),
      ((9,0), (9,1), (8,2), (9,3), (9,4), (8,5), (9,6), (9,7)),
      ((8,8),)
    )
    self.tiles = []
    for team in range(4):
      for picI,picInfo in enumerate(tileList):
        pic = self.tileSprites.get_region(picI*8, team*8, 8, 8)
        for tile in picInfo:
          if team == 1:
            tile = (31-tile[0], tile[1])
          elif team == 2:
            tile = (31-tile[0], 29-tile[1])
          elif team == 3:
            tile = (tile[0], 29-tile[1])
          self.tiles.append(Tile(pic, tile[0]*8+4, tile[1]*8+4))

  def populateTeams(self):
    self.teams = []
    for i in range(4):
      self.teams.append(Team(i, self.tileSprites, self.homeSprites))
