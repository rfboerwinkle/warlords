import pyglet
import pymunk

from Team import *
from Tile import *
from Ball import *

class Game:

  MISC_COLLISION = 0
  BALL_COLLISION = 1
  TILE_COLLISION = 2
  HOME_COLLISION = 3
  SHIELD_COLLISION = 4

  def __init__(self, tileSprites, homeSprites, ballSprites, demo=False):
    self.tileSprites = tileSprites
    self.homeSprites = homeSprites
    self.ballSprites = ballSprites
    self.teams = []
    self.tiles = []
    self.balls = []
    self.space = None

    self.reset()

    if demo:
      pass
    else:
      pass

  def reset(self):
    self.space = pymunk.Space()

    self.populateTeams()
    self.populateTiles()
    self.balls = []
    self.addBall((124, 116), (-500,-500)) # this is temporary

    # borders
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    bottom = pymunk.Poly(body, ((-20,0),(276,0),(-20,-20),(276,-20)))
    bottom.elasticity = 0.9
    top = pymunk.Poly(body, ((-20,240),(276,240),(-20,260),(276,260)))
    top.elasticity = 0.9
    left = pymunk.Poly(body, ((0,-20),(0,260),(-20,-20),(-20,260)))
    left.elasticity = 0.9
    right = pymunk.Poly(body, ((256,-20),(256,260),(276,-20),(276,260)))
    right.elasticity = 0.9
    self.space.add(body, bottom, top, left, right)

    self.space.add_collision_handler(self.BALL_COLLISION, self.TILE_COLLISION).post_solve = self.breakTile
    self.space.add_collision_handler(self.BALL_COLLISION, self.HOME_COLLISION).post_solve = self.breakHome

  def step(self, dt):
    for team in self.teams:
      team.step(dt)
    for ball in self.balls:
      ball.step(dt)
    self.space.step(dt)

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
          body = pymunk.Body(body_type=pymunk.Body.STATIC)
          body.position = (tile[0]*8+4, tile[1]*8+4)
          shape = pymunk.Poly(body, ((-4,4),(4,4),(4,-4),(-4,-4)))
          shape.elasticity = 0.4
          shape.collision_type = self.TILE_COLLISION
          self.space.add(body, shape)
          self.tiles.append(Tile(pic, body))

  def populateTeams(self):
    self.teams = []
    for i in range(4):
      shieldBody = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
      shape = pymunk.Poly(shieldBody, ((-4,4),(4,4),(4,-4),(-4,-4)))
      shape.elasticity = 1.04
      # shape.collision_type = self.SHIELD_COLLISION
      self.space.add(shieldBody, shape)
      homeBody = pymunk.Body(body_type=pymunk.Body.STATIC)
      homeBody.position = ((24,24), (232,24), (232,216), (24,216))[i]
      shape = pymunk.Poly(homeBody, ((-24,-24),(24,-24),(24,24),(-24,24)))
      shape.elasticity = 0.4
      shape.collision_type = self.HOME_COLLISION
      self.space.add(homeBody, shape)
      self.teams.append(Team(i, self.tileSprites, self.homeSprites, shieldBody, homeBody))

  def addBall(self, pos, impulse):
    ball = pymunk.Body(10,100)
    ball.position = pos
    shape = pymunk.Circle(ball, 4, (0,0))
    shape.friction = 0.0
    shape.elasticity = 1
    shape.collision_type = self.BALL_COLLISION
    ball.apply_impulse_at_local_point(impulse)
    self.space.add(ball, shape)
    self.balls.append(Ball(self.ballSprites, ball))

  def breakTile(self, arbiter, space, data):
    _,targetShape = arbiter.shapes
    targetBody = targetShape.body
    for i,tile in enumerate(self.tiles):
      if tile.body is targetBody:
        space.remove(targetShape, targetBody)
        self.tiles.pop(i)
        break

  def breakHome(self, arbiter, space, data):
    _,targetShape = arbiter.shapes
    targetBody = targetShape.body
    for team in self.teams:
      if team.homeBody == targetBody:
        self.space.remove(targetShape, targetBody, team.shieldBody, team.shieldBody.shapes[0])
        team.kill()
        break
