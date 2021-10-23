import numpy as np
from hunter import Hunter
from prey import Prey

from params import board_vars
# from params.py import hunter_vars
# from params.py import prey_vars

import itertools
import csv


class Board:
  def __init__(self, run_num):#, board_vars, hunter_vars, prey_vars):
    # Board is filled with values 0,1,2 for empty, hunter and prey respectively
    self.board_size = board_vars['board_size']
    self.positions = [ [0] * self.board_size for i in range(self.board_size)]
    

    #Initiate the hunters  
    # self.hunter_vars = hunter_vars
    self.hunters = []
    for i in range(board_vars['num_hunters']):
      self.hunters.append(Hunter(self.board_size))#, self.hunter_vars))
    # self.hunters.append(Hunter((23,21)))
    # self.hunters.append(Hunter((21,23)))
    # self.hunters.append(Hunter((8,8)))

    #Initiate the prey 
    # self.prey_vars = prey_vars
    self.prey = []
    for i in range(board_vars['num_prey']):
      self.prey.append(Prey(self.board_size, born = False))#, prey_vars))
    # self.prey.append(Prey((4,4)))
    # self.prey.append(Prey((24,0)))

    for hunter in self.hunters:
      x,y = hunter.get_position()
      self.positions[x][y] = 1

    for p in self.prey:
      x,y = p.get_position()
      self.positions[x][y] = 2

    # Data related stuff:
    self.iteration = 0
    self.max_iterations = board_vars['max_iterations']
    self.data = [[board_vars['num_hunters'], board_vars['num_prey']]]
    self.run_num = run_num

  def print_board(self):
    # Print the list in this order to get a 25x25 grid with [0][0] being bottom left and [24][24] top right
    # Use the symbols when visualizing the board
    symbols = [' ', 'H', 'p']
    for j in range(len(self.positions)-1, -1,-1):
      for i in range(len(self.positions)):
        print(symbols[self.positions[i][j]], end='')
      print('\n')

  def update_board(self):
    # Check which hunters starve
    copied_hunters = []
    for hunter in self.hunters:
      if hunter.get_satedness() < 0:
        # Change the old location to empty
        x,y = hunter.get_position()
        self.positions[x][y] = 0
        # print("a hunter died")
      else:
        copied_hunters.append(hunter)
    self.hunters = copied_hunters

    # Check which agents die of old age
    copied_hunters = []
    for hunter in self.hunters:
      if hunter.get_death_of_age():
        # hunter dies
        # print("hunter dies to age")
        x,y = hunter.get_position()
        self.positions[x][y] = 0
      else:
        hunter.update_age()        
        copied_hunters.append(hunter)
    self.hunters = copied_hunters

    copied_prey = []
    for prey in self.prey:
      if prey.get_death_of_age():
        # prey dies
        # print("prey dies to age")
        x,y = prey.get_position()
        self.positions[x][y] = 0
      else:
        prey.update_age()        
        copied_prey.append(prey)
    self.prey = copied_prey



    # Hunters have small chance to reproduce if they aren't hungry
    for hunters in self.hunters:
      if hunter.check_reproduce():
        self.hunters.append(Hunter(self.board_size))

    # Hungry hunters scan area for prey
    for hunter in self.hunters:
      hunter.search(self.prey)

    # Hunters communicate
    for hunter in self.hunters:
      hunter.communicate(self.hunters)

    # Hunters move, based on their current goal
    new_hunter_pos = []
    for hunter in self.hunters:
      # Change the old locations to empty
      x,y = hunter.get_position()
      self.positions[x][y] = 0
      # Move hunter
      hunter.set_postion(hunter.move(new_hunter_pos, self.hunters))
      new_hunter_pos.append(hunter.get_position())
      x,y = hunter.get_position()
      self.positions[x][y] = 1
        
    # After the hunters have moved, check if they caught a prey
    self.check_alive(new_hunter_pos)


    # Check if prey reproduce
    for prey in self.prey:
      if prey.check_reproduce(self.hunters):
        self.prey.append(Prey(self.board_size, born = True))

    # Determine the new x,y values for the prey, store them and visually update the board
    new_prey_pos = []
    for p in self.prey:
      #Change the old locations to empty
      x,y = p.get_position()
      self.positions[x][y] = 0
      # Move and get the new locations
      p.set_postion(p.move(self.hunters, new_prey_pos))
      new_prey_pos.append(p.get_position())
      x,y = new_prey_pos[-1]
      self.positions[x][y] = 2

    # Update the actual x,y values of the hunters and prey
    for i in range(len(self.hunters)):
      self.hunters[i].set_postion(new_hunter_pos[i])
      # self.check_alive()
    for i in range(len(self.prey)):
      self.prey[i].set_postion(new_prey_pos[i])

    # Updata data file
    self.data.append([len(self.hunters), len(self.prey)])

    # Check if one population has gone extinct, if so: end
    if self.iteration == self.max_iterations or len(self.hunters) == 0 or len(self.prey) == 0:
      # Write data to file
      with open("Results/Run" + str(self.run_num) + ".csv", "w+") as my_csv:
        cs_writer = csv.writer(my_csv, delimiter=',')
        cs_writer.writerows(self.data)
      return False
    else:
      self.iteration += 1
      return True

     

  # Check for each prey if it is in the same position as a hunter
  # If so, remove the prey from the board (its eaten) and reward the hunter
  def check_alive(self, new_hunter_pos):
    eaten_prey = []
    for p in self.prey:
      hunter = 0
      for (x,y) in new_hunter_pos:
        if((x,y) == p.get_position()):
          eaten_prey.append(p)
          self.hunters[hunter].feed(self.hunters)
          break
        hunter += 1
    for eaten_p in eaten_prey:
      self.prey.remove(eaten_p)





    # # Determine the new x,y values for the hunters, store them and visually update the board
    # new_hunter_pos = []
    # for hunter in self.hunters:
    #   # Scan, search for prey
    #   hunter.search()

    #   # collect all goals
    #   goals = []
    #   for hunter in self.hunters:
    #     goals.append(hunter.get_goal())
      
    #   # Every hunter is now aware of all the prey located by the pack of hunters, and chooses closest target
    #   hunter.communicate(goals, self.hunters)


    #   # move



    #   # Change the old locations to empty
    #   x,y = hunter.get_position()
    #   self.positions[x][y] = 0
    #   #Move and get the new locations, hunter moves twice as it is faster
    #   hunter.set_postion(hunter.move(self.prey, new_hunter_pos))
    #   hunter.set_postion(hunter.move(self.prey, new_hunter_pos))
    #   new_hunter_pos.append(hunter.get_position())
    #   # print("hoi")
    #   # print(new_hunter_pos[-1])
    #   x,y = new_hunter_pos[-1]
    #   self.positions[x][y] = 1