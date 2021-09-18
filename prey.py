from random import *

class Prey():
  def __init__(self):
    self.position = (randint(0, 24), randint(0, 24))
    self.critical_Distance = 5


  def getPosition(self):
   return self.position

  def setPostion(self, pos):
    self.position = pos

  def check_move(self, pos):
    x,y = pos

    if x > 24:
      x = 24
    elif x < 0:
      x = 0

    if y > 24:
      y = 24
    elif y < 0:
      y = 0
    
    return (x, y)

  def distance_to_agents(self, hunters):
    distances = []
    x_Self, y_Self = self.position
    for hunter in hunters:
      x_Hunter, y_Hunter = hunter.getPosition()
      distance = (((x_Hunter-x_Self)**2) + ((y_Hunter-y_Self)**2)) **0.5
      distances.append(distance)
      print(x_Self, y_Self)
      print(x_Hunter, y_Hunter)
      print(distance)
      print()

    return distances


  def move(self, hunters):
    # self.position = (randint(0, 24), randint(0, 24))
    distances = self.distance_to_agents(hunters)
    closest_Distance = min(distances)
    closest_Hunter = hunters[distances.index(closest_Distance)]


    x_Self, y_Self = self.position
    x_Hunter, y_Hunter = closest_Hunter.getPosition()
    #If the closest hunter is very close, flee
    if closest_Distance < self.critical_Distance:
      if x_Self > x_Hunter:
        x_Self = x_Self + 1
      elif x_Self < x_Hunter: 
        x_Self = x_Self - 1
      if y_Self > y_Hunter:
        y_Self = y_Self + 1
      elif y_Self < y_Hunter: 
        y_Self = y_Self - 1
    return (self.check_move((x_Self, y_Self)))



