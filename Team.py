import pyglet
import pymunk

class Team:
  def __init__(self, teamIndex, tileSprites, homeSprites, shieldBody, homeBody):
    self.dead = False
    self.teamIndex = teamIndex
    self.shieldBody = shieldBody
    self.homeBody = homeBody
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
    if teamIndex == 2 or teamIndex == 3:
      self.homeY = 240-self.homeY
      self.leftY = 240-self.leftY
      self.rightY = 240-self.rightY

    self.setInterface(None)

  # Returns the angle of the shield
  # True: vertical or "right"
  # False: horizontal or "left"
  def getAngle(self):
    return self.shieldAngle > 0

  def getButton(self):
    if self.interface != None:
      return self.interface[1]()
    return False

  def getShield(self):
    if self.getAngle():
      return (self.rightX, self.leftY + (self.rightY-self.leftY)*self.shieldAngle)
    else:
      return (self.leftX + (self.rightX-self.leftX)*(1+self.shieldAngle), self.leftY)

  def setInterface(self, interface):
    self.interface = interface

  def step(self, dt):
    if self.interface != None:
      self.shieldAngle = self.interface[0]()
    self.shieldBody.position = self.getShield()

  def blit(self):
    if self.interface:
      self.playerHome.blit(self.homeX-24, self.homeY-24, 0)
    else:
      self.aiHome.blit(self.homeX-24, self.homeY-24, 0)
    x,y = self.getShield()
    if self.shieldAngle > 0:
      self.vShield.blit(x-4, y-4, 0)
    else:
      self.hShield.blit(x-4, y-4, 0)

  def kill(self): # real
    self.dead = True
