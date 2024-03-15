import pyglet

class Sprite:
  def __init__(self, pic, body, shape):
    self.pic = pic
    self.body = body
    self.shape = shape
  def blit(self):
    self.pic.blit(self.body.position[0], self.body.position[1], 0)
