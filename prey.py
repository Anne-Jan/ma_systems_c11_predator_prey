from random import *
from params import prey_vars

class Prey():
  def __init__(self, board_size, born = False):
    self.position = (randint(0, board_size-1), randint(0, board_size-1))
    self.critical_distance = prey_vars['prey_vision_range']
    self.board_size = board_size
    self.move_handicap = prey_vars['prey_move_handicap']
    self.reproduce_chance = prey_vars['prey_reproduce_rate']
    if born == True:
      self.age = 0
    else:
      self.age = randint(0, prey_vars['prey_born_max_age'])

  def get_position(self):
   return self.position

  def set_postion(self, pos):
    self.position = pos

  def update_age(self):
    self.age += 1
  
  def get_death_of_age(self):
    return self.age >= prey_vars['prey_max_age']

  def check_move(self, pos):
    x,y = pos

    if x > self.board_size-1:
      x = self.board_size-1
    elif x < 0:
      x = 0

    if y > self.board_size-1:
      y = self.board_size-1
    elif y < 0:
      y = 0
    
    return (x, y)

  def distance_to_agents(self, hunters):
    distances = []
    x_self, y_self = self.position
    for hunter in hunters:
      x_hunter, y_hunter = hunter.get_position()
      distance = (((x_hunter-x_self)**2) + ((y_hunter-y_self)**2)) **0.5
      distances.append(distance)

    return distances

  def check_reproduce(self, hunters):
    if hunters:
      distances = self.distance_to_agents(hunters)
      closest_distance = min(distances)
      if closest_distance < self.critical_distance:
        return False

    chance = uniform(0, 1)
    if chance <= self.reproduce_chance:
      # print("new prey spawned")
      return True
    else:
      return False

  def move(self, hunters, prey):
    # Prey have small chance of not moving at all (to give hunters small advantage)
    chance = uniform(0, 1)
    if chance <= self.move_handicap:
      return self.position

    x_self, y_self = self.position
    no_hunter_close = False
    #If the closest hunter is very close, flee
    if hunters:
      # Check position relative to hunters
      distances = self.distance_to_agents(hunters)
      closest_distance = min(distances)
      if closest_distance < self.critical_distance:
        closest_hunter = hunters[distances.index(closest_distance)]
        
        # If hunter is on the same position, then it is already caught and should not move, so return current position
        x_hunter, y_hunter = closest_hunter.get_position()
        if x_self == x_hunter and y_self == y_hunter:
          return (x_self, y_self)

        if x_self > x_hunter:
          x_self = x_self + 1
        elif x_self < x_hunter: 
          x_self = x_self - 1

        # If the hunter is right behind the prey, move diagonally or in a straight line at random
        else:
          chance = uniform(0, 1)
          if chance <= 0.333:
            x_self += 1
          elif chance <= 0.666:
            x_self -= 1
          # If its larger than 0.666, do not move away but run in a straight line

        if y_self > y_hunter:
          y_self = y_self + 1
        elif y_self < y_hunter: 
          y_self = y_self - 1
        else:
          chance = uniform(0, 1)
          if chance <= 0.333:
            y_self += 1
          elif chance <= 0.666:
            y_self -= 1
      else:
        no_hunter_close = True

    # No hunter is close, roam
    else:
      no_hunter_close = True

    # If no hunter is close: barely move and maybe reproduce
    if no_hunter_close:
      chance = uniform(0, 1)
      if chance <= 0.3:
        x_self += 1
      elif chance <= 0.6:
        x_self -= 1
      chance = uniform(0, 1)
      if chance <= 0.3:
        y_self += 1
      elif chance <= 0.6:
        y_self -= 1
      
    x_self, y_self = self.check_if_occupied(self.check_move((x_self, y_self)), prey)
    return (x_self, y_self)

  def check_if_occupied(self, pos, prey):
    new_x, new_y = pos
    for other_prey_pos in prey:
      if pos == other_prey_pos:
        # print(other_prey_pos)
        # print(pos)
        # print('Possible prey collision')
        
        while((new_x, new_y) == other_prey_pos):
          chance = randint(0,3)
          # print(chance)
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
          
    