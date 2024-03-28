import pyglet
import pymunk
import glsetup

class Tile:
  def __init__(self, pic, body):
    self.pic = pic
    self.body = body
  def blit(self):
    glsetup.blitSetup()
    self.pic.blit(self.body.position[0]-4, self.body.position[1]-4)
