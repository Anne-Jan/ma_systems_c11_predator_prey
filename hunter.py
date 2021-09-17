from random import *

class Hunter:
  def __init__(self):
    self.position = (randint(0, 24), randint(0, 24))

  def getPosition(self):
   return self.position

  def move(self):
    self.position = (randint(0, 24), randint(0, 24))