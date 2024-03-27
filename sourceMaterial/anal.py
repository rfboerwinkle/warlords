"""
import pyglet
from pyglet.gl import *

import os
import sys

assert len(sys.argv) == 2
path = sys.argv[1]
files = os.listdir(path)
files.sort()
files = [os.path.join(path,f) for f in files]
files = [f for f in files if os.path.isfile(f)]
POS = [None for f in files]
assert files

fileI = -1
image = None

Window = pyglet.window.Window(resizable=True)

imgX = 0
imgY = 0
imgScale = 1
imgWidth = 0
imgHeight = 0

out = [[]]

def getPos(dx,dy):
  return ((dx-imgX)//imgScale, (dy-imgY)//imgScale)

def printOut():
  global out
  print()
  for line in out:
    print(line)

def nextImage():
  global files, fileI
  fileI += 1
  if fileI >= len(files):
    fileI = len(files)-1
    print("edge")
  loadImage(files[fileI])

def prevImage():
  global files, fileI
  fileI -= 1
  if fileI < 0:
    fileI = 0
    print("edge")
  loadImage(files[fileI])

def loadImage(imageName):
  global image, imgWidth, imgHeight
  image = pyglet.image.load(imageName)
  imgWidth = image.width
  imgHeight = image.height
  image = image.get_texture()
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  image.width = imgWidth*imgScale
  image.height = imgHeight*imgScale

@Window.event
def on_draw():
  global imgX, imgY, rect
  Window.clear()
  image.blit(imgX, imgY)
  rect.draw()

@Window.event
def on_key_press(symbol, modifiers):
  global out
  if symbol == pyglet.window.key.LEFT:
    prevImage()
  elif symbol == pyglet.window.key.RIGHT:
    nextImage()
  elif symbol == pyglet.window.key.BACKSPACE:
    if out[-1]:
      out[-1].pop()
    elif len(out) != 1:
      out.pop()
    printOut()

@Window.event
def on_mouse_press(x, y, button, modifiers):
  global out
  if button == pyglet.window.mouse.LEFT:
    out[-1].append(getPos(x,y))
    printOut()
  elif button == pyglet.window.mouse.RIGHT:
    if out[-1]:
      out.append([])
    printOut()
@Window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
  global imgX,imgY
  if button == pyglet.window.mouse.MIDDLE:
    imgX += dx
    imgY += dy
  on_mouse_motion(x, y, dx, dy)
@Window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
  global imgScale, imgX, imgY, image, imgWidth, imgHeight
  prev = imgScale
  imgScale += scroll_y
  if imgScale < 1:
    imgScale = 1
  factor = imgScale/prev
  imgX = int(imgX * factor)
  imgY = int(imgY * factor)
  image.width = imgWidth*imgScale
  image.height = imgHeight*imgScale
@Window.event
def on_mouse_motion(x, y, dx, dy):
  global rect, imgX, imgY, imgScale
  x,y = getPos(x,y)
  x = x*imgScale+imgX
  y = y*imgScale+imgY
  rect = pyglet.shapes.Rectangle(x, y, imgScale, imgScale, color=(255,0,0))
  rect.opacity = 100

on_mouse_motion(0,0,0,0)
nextImage()
pyglet.app.run()

 # """

a = [
  [(60, 74)],
  [(86, 102), (113, 130), (139, 158), (156, 179)],
  [(129, 165), (101, 151), (73, 137), (45, 123), (17, 110)],
  [(10, 96), (38, 82)],
  [(57, 99), (71, 133), (86, 166), (101, 199), (115, 232)],
  [(130, 198), (145, 164), (159, 131), (174, 98)],
  [(157, 108), (124, 140), (92, 173)],
  [(89, 181), (117, 165), (145, 149), (173, 133), (201, 117), (229, 102)],
  [(238, 86)],
  [(214, 89), (192, 111), (171, 134), (150, 156), (129, 178)],

  # [(90, 221), (107, 207), (124, 192), (140, 178), (157, 164)],
  # [(146, 152), (129, 141), (112, 130), (96, 119), (79, 108), (62, 97), (45, 85)],
  # [(32, 82), (26, 93), (20, 104), (13, 115), (7, 126), (1, 138)],
  # [(5, 149)],
  # [(3, 149), (1, 143)],
  # [(6, 137), (12, 132), (17, 126), (22, 121), (28, 115), (33, 109), (38, 104), (44, 98), (49, 93), (54, 87), (60, 81), (65, 76), (70, 70)],
  # [(77, 70), (88, 81), (99, 92), (110, 102), (121, 113), (132, 124), (143, 135), (154, 146)],
  # [(160, 157), (144, 172), (127, 187), (110, 202), (94, 218)],
  # [(77, 230)],
  # [(88, 227), (99, 222), (110, 216), (121, 211), (133, 205), (144, 199), (155, 194)],
  # [(160, 159), (138, 140), (115, 122), (93, 103), (70, 84)],
  # [(58, 76)],
  # [(0, 0)],
  # [(0, 0)],
  # [(0, 0)],
  # [(53, 89), (37, 106), (20, 122), (4, 138)],
  # [(11, 155)],
  # [(11, 153), (2, 141)],
  # [(5, 130), (14, 119), (22, 108), (30, 97), (39, 85), (47, 74), (56, 63)],
  # [(51, 69), (46, 74), (41, 80), (37, 85), (32, 91), (27, 97), (22, 102), (18, 108), (13, 113), (8, 119), (3, 124), (0, 130)],
  # [(5, 136), (10, 141), (15, 147), (20, 152)],
  # [(14, 147), (9, 141), (4, 135), (1, 130)],
]

# import math
# for line in a:
#   for i in range(1,len(line)):
#     d = (line[i][0]-line[i-1][0], line[i][1]-line[i-1][1])
#     print(f"({d[0]},{d[1]}, {int(math.degrees(math.atan2(d[1],d[0])))})", end=", ")
#   print()

a = [41,145,120,45,45,135,25,135,53,129,45,129,47,153,65,67,29,133]
a = [min(x,abs(90-x),abs(180-x)) for x in a]
print(a)
print(min(a))
