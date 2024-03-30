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

  def __init__(self, ballSprites, sounds, body):
    self.body = body
    # ball switches every 4 frames
    self.ballPics = tuple(ballSprites.get_region(0, i*8, 8, 8) for i in range(4))
    self.releaseSound = sounds["slide"]
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
    self.grabbed = None
    self.spinning = False

  def blit(self):
    glsetup.blitSetup()
    self.ballPics[self.cycle//4].blit(self.body.position[0], self.body.position[1])
    if self.spinning:
      angle = self.ANGLE[(1,4,7,10)[(self.cycle//2)%4]]
    else:
      target = self.body.velocity.angle_degrees
      for angle in self.ANGLE:
        if abs(angle[0]-target) <= 7.5:
          break

    glsetup.blitSetup()
    self.tailPics[angle[4]][self.cycle//8].get_texture().get_transform(angle[1],angle[2],angle[3]).blit(self.body.position[0], self.body.position[1])

  def step(self, dt):
    self.cycle += 1
    self.cycle %= 16
    if self.grabbed != None:
      toReturn = True
      if self.grabbed[0].shieldBody == None or self.grabbed[0].shieldPressed == False:
        toReturn = False
        self.getReleased()
      if toReturn:
        self.body.position = self.grabbed[0].shieldBody.position
        return

    if self.body.velocity.get_length_sqrd() < 5000:
      self.body.velocity = self.body.velocity.scale_to_length(70.71067811865476)

    if self.body.velocity.get_length_sqrd() > 160000:
      self.body.velocity = self.body.velocity.scale_to_length(400)

    if not self.spinning:
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

  def getGrabbed(self, team, space):
    self.spinning = True
    self.grabbed = (team, space, self.body.shapes)
    space.remove(self.body)
    space.remove(*(x for x in self.body.shapes))

  def getReleased(self):
    try:
      self.releaseSound.play()
    except:
      pass
    self.grabbed[1].add(self.body)
    self.grabbed[1].add(*(x for x in self.grabbed[2]))
    if self.grabbed[0].teamIndex == 0:
      v = pymunk.vec2d.Vec2d(self.body.position[0], self.body.position[1])
    elif self.grabbed[0].teamIndex == 1:
      v = pymunk.vec2d.Vec2d(self.body.position[0]-256, self.body.position[1])
    elif self.grabbed[0].teamIndex == 2:
      v = pymunk.vec2d.Vec2d(self.body.position[0]-256, self.body.position[1]-240)
    elif self.grabbed[0].teamIndex == 3:
      v = pymunk.vec2d.Vec2d(self.body.position[0], self.body.position[1]-240)
    self.body.velocity = v*1000 # this will be normalized in the step, dw bbg
    self.grabbed[0].grabbing = False
    self.grabbed = None
