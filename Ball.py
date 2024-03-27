import pyglet
import pymunk

class Ball:
  def __init__(self, ballSprites, body):
    self.body = body
    self.ballPics = tuple(ballSprites.get_region(0, i*8, 8, 8) for i in range(4))
    # self.tailPics = tuple((spriteSheet.get_region(8, i*8, 8, 8), spriteSheet.get_region(16, i*8, 8, 8)) for i in range(4))
    self.cycle = 0
    self.spinning = False

  def blit(self):
    self.ballPics[self.cycle].blit(self.body.position[0]-4, self.body.position[1]-4, 0)

  def step(self, dt):
    self.cycle += 1
    self.cycle %= 4
