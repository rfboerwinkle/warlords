import pyglet

class Ball:
  def __init__(self):
    self.x = 128
    self.y = 120

  def blit(self):
    self.pic.blit(self.body.position[0]-4, self.body.position[1]-4, 0)

  def step(self, dt):
    pass
