import pyglet
import pymunk
import glsetup

class Ball:

  # angle, flipx, flipy, rotate, base
  ANGLE = (
    (30, False, False, 0, 0),
    (45, False, False, 0, 1),
    (60, True, False, 90, 0),
    (150, True, False, 0, 0),
    (135, True, False, 0, 1),
    (120, False, False, -90, 0),

    (-30, False, True, 0, 0),
    (-45, False, True, 0, 1),
    (-60, True, True, -90, 0),
    (-150, True, True, 0, 0),
    (-135, True, True, 0, 1),
    (-120, False, True, 90, 0),
  )

  def __init__(self, ballSprites, body):
    self.body = body
    # ball switches every 4 frames
    self.ballPics = tuple(ballSprites.get_region(0, i*8, 8, 8) for i in range(4))
    for pic in self.ballPics:
      pic.anchor_x = 4
      pic.anchor_y = 4
    # tail switches every 8 frames
    rawTail = tuple(ballSprites.get_region(8, i*8, 8, 8) for i in range(4))
    # just don't ask
    rawTail[0].anchor_x = 10
    rawTail[0].anchor_y = 6
    rawTail[1].anchor_x = 10
    rawTail[1].anchor_y = 6
    rawTail[2].anchor_x = 8
    rawTail[2].anchor_y = 8
    rawTail[3].anchor_x = 8
    rawTail[3].anchor_y = 8
    self.tailPics = ((rawTail[0],rawTail[1]), (rawTail[2],rawTail[3]))
    self.cycle = 0
    self.spinning = False

  def blit(self):
    glsetup.blitSetup()
    self.ballPics[self.cycle//4].blit(self.body.position[0], self.body.position[1])
    target = self.body.velocity.angle_degrees
    for angle in self.ANGLE:
      if abs(angle[0]-target) <= 7.5:
        glsetup.blitSetup()
        self.tailPics[angle[4]][self.cycle//8].get_texture().get_transform(angle[1],angle[2],angle[3]).blit(self.body.position[0], self.body.position[1])
        break

  def step(self, dt):
    self.cycle += 1
    self.cycle %= 16
    if self.body.velocity.get_length_sqrd() < 5000:
      self.body.velocity = self.body.velocity.scale_to_length(70.71067811865476)

    if self.body.velocity.get_length_sqrd() > 160000:
      self.body.velocity = self.body.velocity.scale_to_length(400)

    angle = self.body.velocity.angle_degrees
    newAngle = None
    BAD = 22.6
    for cardinal in (0,90,180,-90,-180):
      if cardinal-BAD < angle <= cardinal:
        newAngle = cardinal-BAD
        break
      elif cardinal < angle < cardinal+BAD:
        newAngle = cardinal+BAD
        break
    if newAngle:
      self.body.velocity = self.body.velocity.rotated_degrees(newAngle-angle)
