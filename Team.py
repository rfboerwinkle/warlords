import pyglet
import pymunk

class Team:
  def __init__(self, teamIndex, tileSpriteSheet, homeSpriteSheet, shieldBody, homeBody):
    self.dead = False
    self.teamIndex = teamIndex
    self.shieldBody = shieldBody
    self.homeBody = homeBody
    self.shieldAngle = 0
    # [-1,1]
    # -1 is against the vertical wall (left or right, depending)
    # 0 is at the corner
    # 1 is against the horizontal wall
    #
    # I will call -1 "left" and +1 "right", even though it is really CCW and CW
    # (and also only for team 0)

    self.hShield = tileSpriteSheet.get_region(8*8, teamIndex*8, 8, 8)
    self.vShield = tileSpriteSheet.get_region(9*8, teamIndex*8, 8, 8)

    self.homeX = 0
    self.homeY = 0

    self.leftX = 0
    self.rightX = 80
    self.leftY = 80
    self.rightY = 0
    # I know these look a little funky... look at self.shieldAngle, might make a
    # bit more sense.

    if teamIndex == 1 or teamIndex == 2:
      self.homeX = 208-self.homeX
      self.leftX = 248-self.leftX
      self.rightX = 248-self.rightX
    if teamIndex == 2 or teamIndex == 3:
      self.homeY = 192-self.homeY
      self.leftY = 232-self.leftY
      self.rightY = 232-self.rightY

    self.setInterface(None, homeSpriteSheet)

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

  def setInterface(self, interface, homeSpriteSheet):
    self.interface = interface
    if interface:
      self.home = homeSpriteSheet.get_region(48, self.teamIndex*48, 48, 48)
    else:
      self.home = homeSpriteSheet.get_region(0, self.teamIndex*48, 48, 48)

  def step(self):
    if self.interface != None:
      self.shieldAngle = self.interface[0]()
    self.shieldBody.position = self.getShield()

  def blit(self):
    self.home.blit(self.homeX, self.homeY, 0)
    if self.shieldAngle > 0:
      self.vShield.blit(*self.getShield(), 0)
    else:
      self.hShield.blit(*self.getShield(), 0)

  def kill(self): # real
    self.homeBody = None
    self.dead = True
