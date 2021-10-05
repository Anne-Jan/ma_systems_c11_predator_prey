from random import *
import itertools
from params import hunter_vars

class Hunter:
  id_iterator = itertools.count()

  def __init__(self, board_size):
    self.position = (randint(0, board_size-1), randint(0, board_size-1))
    # Range in wich hunters detect prey
    self.critical_distance = hunter_vars['hunter_vision_range']
    self.stalking_distance = hunter_vars['hunter_stalking_range']
    self.board_size = board_size
    self.age = 0

    # Parameters to determine when hunter feels the need to hunt
    self.hunger_threshold = hunter_vars['hunter_hunger_threshold']
    self.satedness = self.hunger_threshold
    self.consumption = hunter_vars['hunter_energy_consumption']
    self.energy_reduc = hunter_vars['hunter_energy_reduc']
    self.goal = None

    # Everything needed for cooperation
    self.id = next(self.id_iterator)
    self.communication_range = hunter_vars['hunter_communication_range']
    self.helping_hunters = []
    self.hunter_to_help = None
    self.is_stalking = False
    self.ready = False
    self.cooperation_energy = hunter_vars['hunter_coop_energy']

    self.reproduce_chance = hunter_vars['hunter_reproduce_rate']

  def get_id(self):
    return self.id

  def update_age(self):
    self.age += 1

  def get_death_of_age(self):
    return self.age >= hunter_vars['hunter_max_age']

  def get_age(self):
    return age

  def get_ready(self):
    return self.ready

  def set_ready(self, status):
    self.ready = status

  def get_waiting(self):
    return self.is_stalking

  def set_waiting(self, status):
    self.is_stalking = status

  def add_helping_hunter(self, helper_id):
    self.helping_hunters.append(helper_id)

  def get_helping_hunters(self):
    return self.helping_hunters

  def get_position(self):
   return self.position

  def set_postion(self, pos):
    self.position = pos

  def get_goal(self):
    return self.goal

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

  def distance(self, pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return (((x2-x1)**2) + ((y2-y1)**2)) **0.5

  def check_reproduce(self):
    if self.satedness > self.hunger_threshold:
      chance = uniform(0, 1)
      if chance <= self.reproduce_chance:
        # print("new hunter spawned")
        return True
      else:
        return False

  def distance_to_agents(self, prey):
    distances = []
    x_self, y_self = self.position
    for p in prey:
      distances.append(self.distance(self.position, p.get_position()))
    return distances

  def search(self, prey):
    if self.satedness > self.hunger_threshold:
      self.goal = None
      # print("I found no prey")
    else:
      distances = self.distance_to_agents(prey)
      closest_distance = min(distances)
      closest_prey = prey[distances.index(closest_distance)]

      if (closest_distance < self.critical_distance):
        self.goal = closest_prey.get_position()
        # print("I found my own prey")
      else:
        # print("I found no prey")
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
            # print("I found a prey through communication")
            self.hunter_to_help = hunters[hunter].get_id()
      hunter += 1
    if best_goal != None:
      self.goal = best_goal
      for hunter in hunters:
        if hunter.get_id() == self.hunter_to_help:
          # Add self to helping hunters of hunter to help
          if self.id not in hunter.get_helping_hunters():
            hunter.add_helping_hunter(self.id)

  def move(self, hunter_positions, hunters):
    x_self, y_self = self.position
    x_original, y_original = self.position
    
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


    else:
      # Hunters by default wait at stalk distance
      distance_to_goal = self.distance(self.position, self.goal)
      if distance_to_goal <= self.stalking_distance:
        self.is_stalking = True
      else:
        self.is_stalking = False


      # Leader waits for all allies to get close
      if len(self.helping_hunters) > 0:
        ready_check = True
        for hunter in hunters:
          for hunter_id in self.helping_hunters:
            if hunter.get_id() == hunter_id:
              if not hunter.get_waiting():
                ready_check = False
        # If all allies are close and waiting, he sets all allies to ready (meaning they will attack prey without ever waiting)
        if ready_check:
          self.ready = True
          for hunter in hunters:
            for hunter_id in self.helping_hunters:
              if hunter.get_id() == hunter_id:
                # hunter.set_waiting_for_go_signal(False)
                # hunter.set_waiting(False)
                hunter.set_ready(True)
                self.is_stalking = False

      # Hunting alone
      if self.hunter_to_help == None and len(self.helping_hunters) == 0:
        self.ready = True


      # Chase targeted prey if no help is coming      
      if distance_to_goal > self.stalking_distance or self.ready:
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
    x_self, y_self = self.check_if_occupied(self.check_move((x_self, y_self)), hunter_positions)

    # Update satedness based on how much hunter moved
    if x_self == x_original and y_self == y_original:
      self.satedness -= (self.energy_reduc * self.consumption) 
    else:
      self.satedness -= self.consumption

    return (x_self, y_self)

  def feed(self, hunters):
    # Recursive function, needs to know if hunter has fed already
    if self.satedness != 100 and self.satedness != self.cooperation_energy:
      if self.hunter_to_help == None and len(self.helping_hunters) == 0:
        self.satedness = 100
      else:
        self.satedness = self.cooperation_energy
      # Every hunter that aided in this hunt gets rewarded:
      for hunter in hunters:
        if hunter.get_id() == self.hunter_to_help:
          hunter.feed(hunters)
        for hunter_id in self.helping_hunters:
          if hunter.get_id() == hunter_id:
            hunter.feed(hunters)
      # print("Nom")
      self.hunter_to_help = None
      self.waiting_for_go_signal = False
      self.helping_hunters = []
      self.is_stalking = False
      self.ready = False

  def get_satedness(self):
    return self.satedness

  def check_if_occupied(self, pos, hunters):
    new_x, new_y = pos
    for other_hunter_pos in hunters:
      if pos == other_hunter_pos:
        
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
          
        pos = (new_x, new_y)
          
    return (new_x, new_y)
