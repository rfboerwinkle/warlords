import math
import random

import pyglet
import pymunk

import glsetup
from Team import *
from Tile import *
from Ball import *

BOUNCE_ELASTICITY = 1.3
FLAT_ELASTICITY = 0.4

class Game:

  MISC_COLLISION = 0
  BALL_COLLISION = 1
  TILE_COLLISION = 2
  HOME_COLLISION = 3
  SHIELD_COLLISION = 4

  IDLE = "idle"
  ONE_PERSON = "one person"
  JOINING = "joining"
  GAMEPLAY = "gameplay"
  DONE = "done"

  def __init__(self, tileSprites, homeSprites, ballSprites, logoSprites, charSprites, dragonSprites, sounds):
    self.tileSprites = tileSprites
    self.homeSprites = homeSprites
    self.ballSprites = ballSprites
    self.logoSprites = logoSprites
    self.sounds = sounds
    def setAnchor(x):
      for elem in x:
        elem.anchor_x = 4
        elem.anchor_y = 4
    self.charSprites = tuple(charSprites.get_region(i*8, 8, 8, 8) for i in range(26))
    setAnchor(self.charSprites)
    self.charSpritesFlipped = tuple(charSprites.get_texture().get_transform(True,True).get_region(i*8, 8, 8, 8) for i in range(26))
    setAnchor(self.charSpritesFlipped)
    self.numbSprites = tuple(charSprites.get_region(i*8, 0, 8, 8) for i in range(10))
    setAnchor(self.numbSprites)
    self.numbSpritesFlipped = tuple(charSprites.get_texture().get_transform(True,True).get_region(i*8, 0, 8, 8) for i in range(10))
    setAnchor(self.numbSpritesFlipped)
    self.teams = []
    self.tiles = []
    self.balls = []
    self.space = None
    self.playerMode = 1 # number of players at start

    self.state = self.IDLE
    self.counter = 0 # this is used for a lot of things, depending on state
    # IDLE: text flashing
    # JOINING: countdown
    # GAMEPLAY: new ball spawn
    # DONE: text flashing
    self.initPhysics()
    self.resetPhysics()

    self.populateTeams()

  def initPhysics(self):
    self.space = pymunk.space.Space()

    WIDTH = 100
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    bottom = pymunk.Poly(body, ((-WIDTH,0),(256+WIDTH,0),(-WIDTH,-WIDTH),(256+WIDTH,-WIDTH)))
    bottom.elasticity = BOUNCE_ELASTICITY
    top = pymunk.Poly(body, ((-WIDTH,240),(256+WIDTH,240),(-WIDTH,240+WIDTH),(256+WIDTH,240+WIDTH)))
    top.elasticity = BOUNCE_ELASTICITY
    left = pymunk.Poly(body, ((0,-WIDTH),(0,240+WIDTH),(-WIDTH,-WIDTH),(-WIDTH,240+WIDTH)))
    left.elasticity = BOUNCE_ELASTICITY
    right = pymunk.Poly(body, ((256,-WIDTH),(256,240+WIDTH),(256+WIDTH,-WIDTH),(256+WIDTH,240+WIDTH)))
    right.elasticity = BOUNCE_ELASTICITY
    self.space.add(body, bottom, top, left, right)

    self.space.add_collision_handler(self.BALL_COLLISION, self.TILE_COLLISION).post_solve = self.breakTile
    self.space.add_collision_handler(self.BALL_COLLISION, self.HOME_COLLISION).pre_solve = self.breakHome
    self.space.add_collision_handler(self.BALL_COLLISION, self.SHIELD_COLLISION).begin = self.shieldCollide
    self.space.add_collision_handler(self.BALL_COLLISION, self.BALL_COLLISION).begin = lambda *x : False

  def resetPhysics(self):
    self.clearBalls()
    self.clearTiles()
    self.clearTeams()

    if len(self.space.bodies) > 1:
      print("uh oh! bodies left!!!", self.space.bodies)
    if len(self.space.shapes) > 4:
      print("uh oh! shapes left!!!", self.space.shapes)

    self.populateTiles()

  def step(self, dt):
    for team in self.teams:
      team.step(dt)
    for ball in self.balls:
      ball.step(dt)

    if self.state == self.IDLE:
      for i,team in enumerate(self.teams):
        if team.rawControls()[1] and team.ai:
          team.ai = False
          self.birthTeam(i)
          self.stateTransition(self.ONE_PERSON)
          break # ik, ik, if they are pressed on the same frame it doesn't work... suck it
    elif self.state == self.ONE_PERSON:
      for i,team in enumerate(self.teams):
        if team.rawControls()[1] and team.ai:
          team.ai = False
          self.birthTeam(i)
          self.stateTransition(self.JOINING)
          break # ik, ik, if they are pressed on the same frame it doesn't work... suck it
    elif self.state == self.JOINING:
      for i,team in enumerate(self.teams):
        if team.rawControls()[1] and team.ai:
          team.ai = False
          self.birthTeam(i)
          break # ik, ik, if they are pressed on the same frame it doesn't work... suck it

    self.counter += 1
    if self.state == self.IDLE:
      self.counter %= 128
    elif self.state == self.ONE_PERSON:
      self.counter %= 128
    elif self.state == self.JOINING:
      if self.counter >= 10*60:
        self.stateTransition(self.GAMEPLAY)
    elif self.state == self.GAMEPLAY:
      if self.counter > 60*60:
        self.counter = 0
        # this will be normalized to the minimum speed
        self.addBall((128, 120), random.uniform(-math.pi, math.pi), 1)
      playersLeft = 0
      aisLeft = 0
      for team in self.teams:
        if not team.isDead():
          if team.ai:
            aisLeft += 1
          else:
            playersLeft += 1
      if self.playerMode == 1:
        if playersLeft == 0 or aisLeft == 0:
          self.stateTransition(self.DONE)
      else:
        if playersLeft == 0:
          self.stateTransition(self.DONE)
        elif playersLeft == 1 and aisLeft == 0:
          self.stateTransition(self.DONE)
    elif self.state == self.DONE:
      if self.counter > 256:
        self.stateTransition(self.IDLE)
    self.space.step(dt)

  def blit(self):
    for tile in self.tiles:
      tile.blit()
    for team in self.teams:
        team.blit()

    if self.state == self.IDLE:
      glsetup.blitSetup()
      self.logoSprites.blit(95, 224)
      self.blitText("WARLORDS"[:self.counter//2], (100,100))
      self.blitText("WARLORDS"[:self.counter//2], (100,100), True)
      self.blitText("PRESS PLAYER START"[:self.counter//2], (60,92))
      self.blitText("PRESS PLAYER START"[:self.counter//2], (60,92), True)
    elif self.state == self.ONE_PERSON:
      self.blitText("MINIMUM OF TWO PLAYERS"[:self.counter//2], (44,100))
      self.blitText("MINIMUM OF TWO PLAYERS"[:self.counter//2], (44,100), True)
      self.blitText("PRESS PLAYER START"[:self.counter//2], (60,92))
      self.blitText("PRESS PLAYER START"[:self.counter//2], (60,92), True)
    elif self.state == self.JOINING:
      self.blitText("PRESS PLAYER START"[:(self.counter%128)//2], (60,92))
      self.blitText("PRESS PLAYER START"[:(self.counter%128)//2], (60,92), True)
      if (600-self.counter)%60 == 0:
        try:
          self.sounds["boom"].play()
        except:
          pass
      self.blitText(str((600-self.counter)//60), (130,60))
      self.blitText(str((600-self.counter)//60), (130,60), True)
    elif self.state == self.GAMEPLAY:
      pass
    elif self.state == self.DONE:
      self.blitText("GAME OVER"[:self.counter//2], (100,108))
      self.blitText("GAME OVER"[:self.counter//2], (100,108), True)

    for ball in self.balls:
      ball.blit()
    # blit dragon

  def blitText(self, text, pos, flipped=False):
    for i,char in enumerate(text):
      o = ord(char)
      if flipped:
        x = (256-pos[0]) - 8*i
        y = 240-pos[1]
      else:
        x = pos[0] + 8*i
        y = pos[1]
      img = None
      if ord("A") <= o <= ord("Z"):
        img = (self.charSpritesFlipped if flipped else self.charSprites)[o-ord("A")]
      elif ord("0") <= o <= ord("9"):
        img = (self.numbSpritesFlipped if flipped else self.numbSprites)[o-ord("0")]
      if img:
        glsetup.blitSetup()
        img.blit(x,y)

  def stateTransition(self, newState):
    if newState == self.IDLE:
      self.counter = 0
      self.resetPhysics()

    elif newState == self.ONE_PERSON:
      self.counter = 0

    elif newState == self.JOINING:
      self.counter = 0

    elif newState == self.GAMEPLAY:
      self.counter = 0
      self.playerMode = 4
      for i,team in enumerate(self.teams):
        if team.isDead():
          self.birthTeam(i)
          self.playerMode -= 1
      self.addBall((124, 116), random.uniform(-math.pi, math.pi), 200)

    elif newState == self.DONE:
      self.sounds["fanfare"].play()
      self.counter = 0
      self.clearBalls()

    self.state = newState

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
          shape.elasticity = FLAT_ELASTICITY
          shape.collision_type = self.TILE_COLLISION
          self.space.add(body, shape)
          self.tiles.append(Tile(pic, body))

  def populateTeams(self):
    self.teams = []
    for i in range(4):
      self.teams.append(Team(i, self.tileSprites, self.homeSprites, self))

  def addBall(self, pos, angle, mag):
    try:
      self.sounds["slide"].play()
    except:
      pass
    ball = pymunk.Body(10,100)
    ball.position = pos
    ball.velocity = pymunk.vec2d.Vec2d(math.cos(angle)*mag, math.sin(angle)*mag)
    shape = pymunk.Circle(ball, 4, (0,0))
    shape.friction = 0.0
    shape.elasticity = 1
    shape.collision_type = self.BALL_COLLISION
    self.space.add(ball, shape)
    self.balls.append(Ball(self.ballSprites, self.sounds, ball))

  def clearBalls(self):
    for ball in self.balls:
      self.space.remove(ball.body)
      self.space.remove(*(x for x in ball.body.shapes))
    self.balls = []

  def clearTiles(self):
    for tile in self.tiles:
      self.space.remove(tile.body)
      self.space.remove(*(x for x in tile.body.shapes))
    self.tiles = []

  def clearTeams(self):
    for i,team in enumerate(self.teams):
      if not team.isDead():
        self.killTeam(i, peaceful=True)
      team.ai = True

  def breakTile(self, arbiter, space, data):
    try:
      self.sounds["triangle"].play()
    except:
      pass
    targetBall,targetShape = arbiter.shapes
    for ball in self.balls:
      if ball.body == targetBall.body:
        ball.spinning = False
        break
    targetBody = targetShape.body
    for i,tile in enumerate(self.tiles):
      if tile.body is targetBody:
        space.remove(targetShape, targetBody)
        self.tiles.pop(i)
        break

  def breakHome(self, arbiter, space, data):
    try:
      self.sounds["explosion"].play()
    except:
      pass
    targetBall,targetShape = arbiter.shapes
    for ball in self.balls:
      if ball.body == targetBall.body:
        break
    targetBody = targetShape.body
    for i,team in enumerate(self.teams):
      if team.homeBody == targetBody:
        self.addBall(ball.body.position, ball.body.velocity.angle, ball.body.velocity.length)
        self.killTeam(i)
        break
    return True

  def shieldCollide(self, arbiter, space, data):
    try:
      self.sounds["boom"].play()
    except:
      pass
    targetBall, targetShape = arbiter.shapes
    for ball in self.balls:
      if ball.body == targetBall.body:
        break
    targetBody = targetShape.body
    for team in self.teams:
      if team.shieldBody == targetBody:
        if team.shieldPressed and not team.grabbing:
          team.grabbing = True
          ball.getGrabbed(team, self.space)
          return False
        break
    return True

  def killTeam(self, i, peaceful=False):
    team = self.teams[i]
    self.space.remove(team.homeBody, team.shieldBody)
    self.space.remove(*(x for x in team.homeBody.shapes))
    self.space.remove(*(x for x in team.shieldBody.shapes))
    team.die(peaceful=peaceful)

  def birthTeam(self, i):
    shieldBody = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    shape = pymunk.Poly(shieldBody, ((-4,4),(4,4),(4,-4),(-4,-4)))
    shape.elasticity = BOUNCE_ELASTICITY
    shape.collision_type = self.SHIELD_COLLISION
    self.space.add(shieldBody, shape)
    homeBody = pymunk.Body(body_type=pymunk.Body.STATIC)
    homeBody.position = ((24,24), (232,24), (232,216), (24,216))[i]
    shape = pymunk.Poly(homeBody, ((-24,-24),(24,-24),(24,24),(-24,24)))
    shape.elasticity = BOUNCE_ELASTICITY
    shape.collision_type = self.HOME_COLLISION
    self.space.add(homeBody, shape)
    self.teams[i].homeBody = homeBody
    self.teams[i].shieldBody = shieldBody
    self.teams[i].birth()
