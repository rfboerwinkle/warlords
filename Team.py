import math

import pyglet
import pymunk

import glsetup

class Team:
  def __init__(self, teamIndex, tileSprites, homeSprites, game):
    self.deadCounter = 24*4 + 1
    self.teamIndex = teamIndex
    self.ai = True

    self.game = game

    self.shieldBody = None
    self.homeBody = None

    self.grabbing = False
    self.joystick = None
    self.shieldPressed = False
    self.shieldAngle = 0
    # [-1,1]
    # -1 is against the vertical wall (left or right, depending)
    # 0 is at the corner
    # 1 is against the horizontal wall

    # I will call -1 "left" and +1 "right", even though it is really CCW and CW
    # (and also only for team 0)

    self.hShield = tileSprites.get_region(8*8, teamIndex*8, 8, 8)
    self.vShield = tileSprites.get_region(9*8, teamIndex*8, 8, 8)

    self.playerHome = homeSprites.get_region(48, self.teamIndex*48, 48, 48)
    self.aiHome = homeSprites.get_region(0, self.teamIndex*48, 48, 48)

    self.explodePics = (
      homeSprites.get_region(80, 216, 16, 16),
      homeSprites.get_region(72, 192, 24, 24),
      homeSprites.get_region(40, 192, 32, 32),
      homeSprites.get_region(0, 192, 40, 40),
    )

    self.homeX = 24
    self.homeY = 24

    self.leftX = 4
    self.rightX = 84
    self.leftY = 84
    self.rightY = 4
    # I know these look a little funky... look at self.shieldAngle, might make a
    # bit more sense.

    if teamIndex == 1 or teamIndex == 2:
      self.homeX = 256-self.homeX
      self.leftX = 256-self.leftX
      self.rightX = 256-self.rightX
      for i,pic in enumerate(self.explodePics):
          pic.anchor_x = i*8 - 8
    else:
      for i,pic in enumerate(self.explodePics):
          pic.anchor_x = 24

    if teamIndex == 2 or teamIndex == 3:
      self.homeY = 240-self.homeY
      self.leftY = 240-self.leftY
      self.rightY = 240-self.rightY
      for i,pic in enumerate(self.explodePics):
        pic.anchor_y = i*8 - 8
    else:
      for i,pic in enumerate(self.explodePics):
        pic.anchor_y = 24

  def rawControls(self):
    angle = 0
    pressed = False
    if self.joystick:
      angle = self.joystick.x if self.teamIndex%2 else -self.joystick.y
      pressed = self.joystick.buttons[0] if self.teamIndex%2 else self.joystick.buttons[1]
    return angle,pressed

  def updateControls(self):
    if self.isDead():
      self.shieldAngle = 0
      self.shieldPressed = False
      return

    if self.ai:
      self.shieldPressed = False
      origin = ((0,0), (256,0), (256,240), (0,240))[self.teamIndex]
      goal = 0
      minDistance = 1000000
      for ball in self.game.balls:
        pos = ball.body.position
        dist = (pos[0]-origin[0])**2 + (pos[0]-origin[0])**2
        if dist < minDistance:
          minDistance = dist
          goal = math.atan2(ball.body.position[1]-origin[1], ball.body.position[0]-origin[0])
      angleConvert = ((math.pi/2,0), (math.pi/2, math.pi), (-math.pi/2, -math.pi), (-math.pi/2, 0))[self.teamIndex]
      goal = ((goal-angleConvert[0])/(angleConvert[1]-angleConvert[0]))*2-1
      goal = goal-self.shieldAngle
      if goal > 0.05:
        self.shieldAngle += 0.01
      elif goal < -0.05:
        self.shieldAngle -= 0.01

    else:
      self.shieldAngle, self.shieldPressed = self.rawControls()

  # Returns the angle of the shield
  # True: vertical or "right"
  # False: horizontal or "left"
  def getAngle(self):
    return self.shieldAngle > 0

  def getShield(self):
    if self.getAngle():
      return (self.rightX, self.leftY + (self.rightY-self.leftY)*self.shieldAngle)
    else:
      return (self.leftX + (self.rightX-self.leftX)*(1+self.shieldAngle), self.leftY)

  def step(self, dt):
    if self.deadCounter == -1:
      self.updateControls()
      self.shieldBody.position = self.getShield()
    elif self.deadCounter != 24*4 + 1:
      self.deadCounter += 1

  def blit(self):
    # alive
    if self.deadCounter == -1:
      glsetup.blitSetup()
      if self.ai:
        self.aiHome.blit(self.homeX-24, self.homeY-24)
      else:
        self.playerHome.blit(self.homeX-24, self.homeY-24)
      x,y = self.getShield()
      glsetup.blitSetup()
      if self.shieldAngle > 0:
        self.vShield.blit(x-4, y-4)
      else:
        self.hShield.blit(x-4, y-4)

    # dying
    elif self.deadCounter <= 24*4:
      frame = self.deadCounter//4
      if frame <= 3:
        glsetup.blitSetup()
        if self.ai:
          self.aiHome.blit(self.homeX-24, self.homeY-24)
        else:
          self.playerHome.blit(self.homeX-24, self.homeY-24)

      explodeFrame = (0,1,2,3,2,1,0,-1)[frame%8]
      if explodeFrame != -1:
        glsetup.blitSetup()
        self.explodePics[explodeFrame].blit(self.homeX, self.homeY)

  def die(self, peaceful = False): # real
    self.homeBody = None
    self.shieldBody = None
    self.grabbing = False
    if peaceful:
      self.deadCounter = 24*4 + 1
    else:
      self.deadCounter = 0

  def birth(self): # realer
    self.deadCounter = -1

  def isDead(self):
    return self.deadCounter != -1
