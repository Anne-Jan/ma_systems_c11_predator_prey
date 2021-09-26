from random import *

class Hunter:
  def __init__(self, pos  = None):
    self.position = pos if pos is not None else (randint(0, 24), randint(0, 24))
    self.critical_distance = 20

    # Parameters to determine when hunter feels the need to hunt
    self.hunger_threshold = 60
    self.satedness = 60
    self.consumption = 5

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

  def distance_to_agents(self, prey):
    distances = []
    x_self, y_self = self.position
    for p in prey:
      x_prey, y_prey = p.get_position()
      distance = (((x_prey-x_self)**2) + ((y_prey-y_self)**2)) **0.5
      distances.append(distance)

    return distances


  def move(self, prey, hunters):
    # self.position = (randint(0, 24), randint(0, 24))
    distances = self.distance_to_agents(prey)
    closest_distance = min(distances)
    closest_prey = prey[distances.index(closest_distance)]


    x_self, y_self = self.position
    x_prey, y_prey = closest_prey.get_position()
    # If the closest prey is very close and hunter is hungry, hunt
    if (closest_distance < self.critical_distance) and (self.satedness < self.hunger_threshold):
      if x_self > x_prey:
        x_self = x_self - 1
      elif x_self < x_prey: 
        x_self = x_self + 1
      if y_self > y_prey:
        y_self = y_self - 1
      elif y_self < y_prey: 
        y_self = y_self + 1

    # No prey is close, or not hungry: roam, with a large chance to move randomly instead of staying in place
    else:
      chance = uniform(0, 1)
      if chance <= 0.4:
        x_self += 1
      elif chance <= 0.8:
        x_self -= 1
      chance = uniform(0, 1)
      if chance <= 0.4:
        y_self += 1
      elif chance <= 0.8:
        y_self -= 1


    x_self, y_self = self.check_if_occupied(self.check_move((x_self, y_self)), hunters)

    self.satedness -= self.consumption
    return (x_self, y_self)

  def feed(self):
    self.satedness = 100
    print("Nom")

  def get_satedness(self):
    return self.satedness

  def check_if_occupied(self, pos, hunters):
    new_x, new_y = pos
    for other_hunter_pos in hunters:
      if pos == other_hunter_pos:
        # print(other_hunter_pos)
        # print(pos)
        print('Possible hunter collision')
        
        while((new_x, new_y) == other_hunter_pos):
          chance = randint(0,3)
          if chance == 0:
            new_x += 1
          elif chance  == 1:
            new_x -= 1
          elif chance == 2:
            new_y += 1
          else:
            new_y -= 1
          #Check if this new position is legal and, if it is not legal, the pos was modified to the original pos by the check_move function
          #If the pos turned to be unchanged, try again  
          (new_x, new_y) = self.check_move((new_x, new_y))
          # print(other_hunter_pos)
          # print((new_x, new_y))
          # if((new_x, new_y) != other_hunter_pos):
            # break
        pos = (new_x, new_y)
          
    return (new_x, new_y)
