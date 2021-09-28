from random import *

class Hunter:
  def __init__(self, pos  = None):
    self.position = pos if pos is not None else (randint(0, 24), randint(0, 24))
    # Range in wich hunters detect prey
    self.critical_distance = 10
    # Range in which hunters can communicate
    self.communication_range = 10000

    # Parameters to determine when hunter feels the need to hunt
    self.hunger_threshold = 90
    self.satedness = 60
    self.consumption = 1
    self.goal = None

  def get_position(self):
   return self.position

  def set_postion(self, pos):
    self.position = pos

  def get_goal(self):
    return self.goal

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

  def distance(self, pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return (((x2-x1)**2) + ((y2-y1)**2)) **0.5


  def distance_to_agents(self, prey):
    distances = []
    x_self, y_self = self.position
    for p in prey:
      # x_prey, y_prey = p.get_position()
      # distance = (((x_prey-x_self)**2) + ((y_prey-y_self)**2)) **0.5
      # distances.append(distance)
      distances.append(self.distance(self.position, p.get_position()))
    return distances

  def search(self, prey):
    if self.satedness > self.hunger_threshold:
      self.goal = None
      print("I found no prey")
    else:
      distances = self.distance_to_agents(prey)
      closest_distance = min(distances)
      closest_prey = prey[distances.index(closest_distance)]

      if (closest_distance < self.critical_distance):
        self.goal = closest_prey.get_position()
        print("I found my own prey")
      else:
        print("I found no prey")
        self.goal = None

  def communicate(self, hunters):
    if (self.goal != None) or (self.satedness > self.hunger_threshold):
      return

    # Check goals of hunters in communication range
    distances_to_hunters = self.distance_to_agents(hunters)
    best_goal = None
    best_goal_distance = 999999
    hunter = 0

    # If hunter is in communication range, change goal to that hunter's goal if it is better than currently selected goal
    for distance in distances_to_hunters:
      if distance < self.communication_range:
        temp_goal = hunters[hunter].get_goal()
        if temp_goal != None:
          goal_distance = self.distance(self.position, temp_goal)
          if goal_distance < best_goal_distance:
            best_goal = temp_goal
            print("I found a prey through communication")
      hunter += 1
    if best_goal != None:
      self.goal = best_goal

  def move(self, hunters):
    x_self, y_self = self.position

    # No goal obtained: either not hungry or no prey found
    if self.goal == None:
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

    # Chase targeted prey
    else:
      x_prey, y_prey = self.goal
      if x_self > x_prey:
        x_self = x_self - 1
      elif x_self < x_prey: 
        x_self = x_self + 1
      if y_self > y_prey:
        y_self = y_self - 1
      elif y_self < y_prey: 
        y_self = y_self + 1


    # Check if move is legal
    x_self, y_self = self.check_if_occupied(self.check_move((x_self, y_self)), hunters)

    # Update satedness
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
