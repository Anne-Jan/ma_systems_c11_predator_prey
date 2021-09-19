from random import *

class Hunter:
  def __init__(self, pos):
    # self.position = (randint(0, 24), randint(0, 24))
    self.position = pos
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

    return distances


  def move(self, prey, hunters):
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

     #no prey is close, roam, but with a larger chance to move instead of stay in place
    else:
      chance = uniform(0, 1)
      if chance <= 0.4:
        x_Self += 1
      elif chance <= 0.8:
        x_Self -= 1
      chance = uniform(0, 1)
      if chance <= 0.4:
        y_Self += 1
      elif chance <= 0.8:
        y_Self -= 1


    x_Self, y_Self = self.check_if_occupied((x_Self, y_Self), hunters)
    return (self.check_move((x_Self, y_Self)))

  def check_if_occupied(self, pos, hunters):
    new_X, new_Y = pos
    for other_hunter_pos in hunters:
      if pos == other_hunter_pos:
        print(other_hunter_pos)
        print(pos)
        print('TEST')
        
        while(True):
          chance = randint(0,3)
          if chance == 0:
            new_X += 1
          elif chance  == 1:
            new_X -= 1
          elif chance == 2:
            new_Y += 1
          else:
            new_Y -= 1
          #Check if this new position is legal and, if it is not legal, the pos was modified to the original pos by the check_move function
          #If the pos turned to be unchanged, try again  
          (new_X, new_Y) = self.check_move((new_X, new_Y))
          print(other_hunter_pos)
          print((new_X, new_Y))
          if((new_X, new_Y) != other_hunter_pos):
            break
          
    return (new_X, new_Y)
