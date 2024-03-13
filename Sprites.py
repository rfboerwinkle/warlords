import pyglet

class Sprite:
  def __init__(self, pic, x, y):
    self.pic = pic
    self.x = x
    self.y = y
  def blit(self):
    self.pic.blit(self.x, self.y, 0)

def populateTiles(spriteSheet):
  tileList = (
    ((7,0), (6,0), (7,1), (6,1), (7,2), (6,2), (7,3), (6,3), (7,4), (6,4), (7,5), (6,5), (7,6), (6,6), (7,7), (6,7), (5,7), (5,6), (4,7), (4,6), (3,7), (3,6), (2,7), (2,6), (1,7), (1,6), (0,7), (0,6)),
    ((0,8), (3,8), (6,8)),
    ((1,8), (4,8), (7,8)),
    ((0,9), (1,9), (2,8), (3,9), (4,9), (5,8), (6,9), (7,9)),
    ((8,0), (8,3), (8,6)),
    ((8,1), (8,4), (8,7)),
    ((9,0), (9,1), (8,2), (9,3), (9,4), (8,5), (9,6), (9,7)),
    ((8,8),)
  )
  tiles = []
  for team in range(4):
    for picI,picInfo in enumerate(tileList):
      pic = spriteSheet.get_region(picI*8, team*8, 8, 8)
      for tile in picInfo:
        if team == 1:
          tile = (31-tile[0], tile[1])
        elif team == 2:
          tile = (31-tile[0], 29-tile[1])
        elif team == 3:
          tile = (tile[0], 29-tile[1])
        tiles.append(Sprite(pic, tile[0]*8, tile[1]*8))
  return tiles
