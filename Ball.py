import pyglet
import pymunk
import glsetup

class Ball:
  def __init__(self, ballSprites, body):
    self.body = body
    # ball switches every 4 frames
    self.ballPics = tuple(ballSprites.get_region(0, i*8, 8, 8) for i in range(4))
    # tail switches every 8 frames
    # self.tailPics = tuple((spriteSheet.get_region(8, i*8, 8, 8), spriteSheet.get_region(16, i*8, 8, 8)) for i in range(4))
    self.cycle = 0
    self.spinning = False

  def blit(self):
    glsetup.blitSetup()
    self.ballPics[self.cycle//4].blit(self.body.position[0]-4, self.body.position[1]-4, 0)

  def step(self, dt):
    self.cycle += 1
    self.cycle %= 16
    if self.body.velocity.get_length_sqrd() < 5000:
      self.body.velocity = self.body.velocity.scale_to_length(70.71067811865476)

    if self.body.velocity.get_length_sqrd() > 200000:
      self.body.velocity = self.body.velocity.scale_to_length(447.21359549995793)

    angle = self.body.velocity.angle_degrees
    newAngle = None
    BAD = 23
    for cardinal in (0,90,180,-90,-180):
      if cardinal-BAD < angle <= cardinal:
        newAngle = cardinal-BAD
        break
      elif cardinal < angle < cardinal+BAD:
        newAngle = cardinal+BAD
        break
    if newAngle:
      self.body.velocity = self.body.velocity.rotated_degrees(newAngle-angle)
