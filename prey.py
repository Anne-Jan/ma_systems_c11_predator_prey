from random import *

class Prey():
  def __init__(self, pos = None):
    self.position = pos if pos is not None else (randint(0, 24), randint(0, 24))
    self.critical_Distance = 5


  def get_position(self):
   return self.position

  def set_postion(self, pos):
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
      x_Hunter, y_Hunter = hunter.get_position()
      distance = (((x_Hunter-x_Self)**2) + ((y_Hunter-y_Self)**2)) **0.5
      distances.append(distance)

    return distances


  def move(self, hunters, prey):
    # self.position = (randint(0, 24), randint(0, 24))
    distances = self.distance_to_agents(hunters)
    closest_Distance = min(distances)
    closest_Hunter = hunters[distances.index(closest_Distance)]


    x_Self, y_Self = self.position
    x_Hunter, y_Hunter = closest_Hunter.get_position()
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
        # If its larger than 0.666, do not move away but run in a straight line

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


    # No hunter is close, roam
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
      
    x_Self, y_Self = self.check_if_occupied(self.check_move((x_Self, y_Self)), prey)
    return (x_Self, y_Self)

  def check_if_occupied(self, pos, prey):
    new_x, new_y = pos
    for other_prey_pos in prey:
      if pos == other_prey_pos:
        # print(other_prey_pos)
        # print(pos)
        print('Possible prey collision')
        
        while((new_x, new_y) == other_prey_pos):
          chance = randint(0,3)
          print(chance)
          if chance == 0:
            new_x += 1
          elif chance  == 1:
            new_x -= 1
          elif chance == 2:
            new_y += 1
          else:
            new_y -=  1
          # Check if this new position is legal and, if it is not legal, the pos was modified to the original pos by the check_move function
          # If the pos turned to be unchanged, try again  
          (new_x, new_y) = self.check_move((new_x, new_y))
          print(other_prey_pos)
          print((new_x, new_y))
          # if((new_x, new_y) != other_prey_pos):
          #   break
        pos = (new_x, new_y)
    return pos















  # def check_if_occupied_base(self, pos, prey):
  #   for other_prey_pos in prey:
  #     if pos == other_prey_pos:
  #       check_if_occupied_rec(pos, prey)
  #   return pos

  # def check_if_occupied_rec(self, pos, prey):
  #   if (pos != prey):
  #     return pos
  #   else:
  #     while (pos == prey[index]):
  #       x,y = pos
  #       chance = randint(0,3)
  #       print(chance)
  #       if chance == 0:
  #         x += 1
  #       elif chance  == 1:
  #         x -= 1
  #       elif chance == 2:
  #         y += 1
  #       else:
  #         y -=  1
  #       (x,y) = self.check_move((x,y))
  #       pos = (x,y)
  #     index += 1
  #     return check_if_occupied_rec(pos, prey, index)

    # for other_prey_pos in prey:
    #   if pos == other_prey_pos:
    #     # print(other_prey_pos)
    #     # print(pos)
    #     print('Possible prey collision')
        
    #     while((new_x, new_y) == other_prey_pos):
    #       chance = randint(0,3)
    #       print(chance)
    #       if chance == 0:
    #         new_x += 1
    #       elif chance  == 1:
    #         new_x -= 1
    #       elif chance == 2:
    #         new_y += 1
    #       else:
    #         new_y -=  1
    #       # Check if this new position is legal and, if it is not legal, the pos was modified to the original pos by the check_move function
    #       # If the pos turned to be unchanged, try again  
    #       (new_x, new_y) = self.check_move((new_x, new_y))
    #       print(other_prey_pos)
    #       print((new_x, new_y))
    #       # if((new_x, new_y) != other_prey_pos):
    #       #   break
          
    