from random import *

class Prey():
  def __init__(self, pos):
    # self.position = (randint(0, 24), randint(0, 24))
    self.position = pos
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

    return distances


  def move(self, hunters, prey):
    # self.position = (randint(0, 24), randint(0, 24))
    distances = self.distance_to_agents(hunters)
    closest_Distance = min(distances)
    closest_Hunter = hunters[distances.index(closest_Distance)]


    x_Self, y_Self = self.position
    x_Hunter, y_Hunter = closest_Hunter.getPosition()
    #If the closest hunter is very close, flee
    if closest_Distance < self.critical_Distance:
      ###If hunter is on the same position, then it is already caught and should not move, so return current position
      if x_Self == x_Hunter and y_Self == y_Hunter:
        return (x_Self, y_Self)

      if x_Self > x_Hunter:
        x_Self = x_Self + 1
      elif x_Self < x_Hunter: 
        x_Self = x_Self - 1

      #if the hunter is right behind the prey, move diagonally or in a straight line at random
      else:
        chance = uniform(0, 1)
        if chance <= 0.333:
          x_Self += 1
        elif chance <= 0.666:
          x_Self -= 1
        ##if its larger than 0.666, do not move away but run in a straight line



      if y_Self > y_Hunter:
        y_Self = y_Self + 1
      elif y_Self < y_Hunter: 
        y_Self = y_Self - 1
      else:
        chance = uniform(0, 1)
        if chance <= 0.333:
          y_Self += 1
        elif chance <= 0.666:
          y_Self -= 1
    #no hunter is close, roam
    else:
      chance = uniform(0, 1)
      if chance <= 0.3:
        x_Self += 1
      elif chance <= 0.6:
        x_Self -= 1
      chance = uniform(0, 1)
      if chance <= 0.3:
        y_Self += 1
      elif chance <= 0.6:
        y_Self -= 1
      
    x_Self, y_Self = self.check_if_occupied((x_Self, y_Self), prey)
    return (self.check_move((x_Self, y_Self)))

  def check_if_occupied(self, pos, prey):
    new_X, new_Y = pos
    for other_prey_pos in prey:
      if pos == other_prey_pos:
        print(other_prey_pos)
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
            new_Y -=  1
          #Check if this new position is legal and, if it is not legal, the pos was modified to the original pos by the check_move function
          #If the pos turned to be unchanged, try again  
          (new_X, new_Y) = self.check_move((new_X, new_Y))
          print(other_prey_pos)
          print((new_X, new_Y))
          if((new_X, new_Y) != other_prey_pos):
            break
          
    return (new_X, new_Y)


