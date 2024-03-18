import pyglet

class Tile:
  def __init__(self, pic, x, y):
    self.pic = pic
    self.x = x
    self.y = y
  def blit(self):
    self.pic.blit(self.x-4, self.y-4, 0)
