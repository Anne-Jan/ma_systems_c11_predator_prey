from random import *

class Hunter:
  def __init__(self):
    self.position = (randint(0, 24), randint(0, 24))
    self.critical_Distance = 20

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

  def distance_to_agents(self, prey):
    distances = []
    x_Self, y_Self = self.position
    for p in prey:
      x_Prey, y_Prey = p.getPosition()
      distance = (((x_Prey-x_Self)**2) + ((y_Prey-y_Self)**2)) **0.5
      distances.append(distance)
      print(x_Self, y_Self)
      print(x_Prey, y_Prey)
      print(distance)
      print()

    return distances


  def move(self, prey):
    # self.position = (randint(0, 24), randint(0, 24))
    distances = self.distance_to_agents(prey)
    closest_Distance = min(distances)
    closest_Prey = prey[distances.index(closest_Distance)]


    x_Self, y_Self = self.position
    x_Prey, y_Prey = closest_Prey.getPosition()
    #If the closest prey is very close, hunt
    if closest_Distance < self.critical_Distance:
      if x_Self > x_Prey:
        x_Self = x_Self - 1
      elif x_Self < x_Prey: 
        x_Self = x_Self + 1
      if y_Self > y_Prey:
        y_Self = y_Self - 1
      elif y_Self < y_Prey: 
        y_Self = y_Self + 1
    return (self.check_move((x_Self, y_Self)))
