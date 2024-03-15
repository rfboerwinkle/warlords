import pyglet
import pymunk

from Team import *
from Sprite import *

class Game:

  MISC_COLLISION = 0
  BALL_COLLISION = 1
  TILE_COLLISION = 2

  def __init__(self, tileSprites, homeSprites, demo=False):
    self.tileSprites = tileSprites
    self.homeSprites = homeSprites
    self.tiles = []
    self.teams = []
    self.space = None
    self.reset()

    if demo:
      pass
    else:
      pass

  def reset(self):
    self.space = pymunk.Space()

    self.populateTiles()
    self.populateTeams()

    self.ball = pymunk.Body(10,100)
    self.ball.position = (124, 116)
    shape = pymunk.Circle(self.ball, 4, (0,0))
    shape.friction = 0.0
    shape.elasticity = 1.2
    shape.collision_type = self.BALL_COLLISION
    self.ball.apply_impulse_at_local_point((200,200))
    self.space.add(self.ball, shape)

    self.space.add_collision_handler(self.BALL_COLLISION, self.TILE_COLLISION).post_solve = self.breakTile
    # self.space.add_default_collision_handler().pre_solve = self.a
  def a(self,a,b,c):
    print(a,b,c)
    return True

  def step(self, dt):
    # print(dt)
    for team in self.teams:
      team.step()
    self.space.step(dt)

  # ball argument is temp
  def blit(self, ball):
    for tile in self.tiles:
      tile.blit()
    for team in self.teams:
      team.blit()
    ball.blit(self.ball.position[0], self.ball.position[1], 0)

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
          body = pymunk.Body(body_type=pymunk.Body.STATIC)
          body.position = (tile[0]*8, tile[1]*8)
          shape = pymunk.Poly(body, ((-4,4),(4,4),(4,-4),(-4,-4)))
          shape.elasticity = 0.9
          shape.collision_type = self.TILE_COLLISION
          self.space.add(body, shape)
          self.tiles.append(Sprite(pic, body, shape))

  def populateTeams(self):
    self.teams = [Team(i, self.tileSprites, self.homeSprites) for i in range(4)]

  def breakTile(self,arbiter, space, data):
    ball,tile = arbiter.shapes
    print("goooooood")
    print(ball, tile)
    for i,sprite in enumerate(self.tiles):
      if sprite.shape is tile:
        space.remove(sprite.shape, sprite.body)
        self.tiles.pop(i)
        break
    # return False
