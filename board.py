import numpy as np
from hunter import Hunter
from prey import Prey
import itertools

class Board:
  def __init__(self, num_hunters, num_prey):
    #Board is filled with values 0,1,2 for empty, hunter and prey respectively
    #Use the symbols when visualizing the board
    self.symbols = [' | | ', ' |H| ', ' |p| ']

    self.positions = [ [0] * 25 for i in range(25)]


    #Initiate the hunters  
    self.hunters = []
    for i in range(num_hunters):
      self.hunters.append(Hunter())
      
    #Initiate the prey 
    self.prey = []
    for i in range(num_prey):
      self.prey.append(Prey())

    for hunter in self.hunters:
      x,y = hunter.get_position()
      self.positions[x][y] = 1

    for p in self.prey:
      x,y = p.get_position()
      self.positions[x][y] = 2


  def print_board(self):
    #Print the list in this order to get a 25x25 grid with [0][0] being bottom left and [24][24] top right
    for j in range(len(self.positions)-1, -1,-1):
      for i in range(len(self.positions)):
        print(self.symbols[self.positions[i][j]], end='')
      print('\n')

  def update_board(self):
    # Check which hunters starve
    copied_hunters = []
    for hunter in self.hunters:
      if hunter.get_satedness() < 0:
        # Change the old location to empty
        x,y = hunter.get_position()
        self.positions[x][y] = 0
        print("a hunter died")
      else:
        copied_hunters.append(hunter)
    self.hunters = copied_hunters

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
      #Move and get the new locations, hunter moves twice as it is faster
      hunter.set_postion(hunter.move(new_hunter_pos))
      # hunter.set_postion(hunter.move(new_hunter_pos))
      new_hunter_pos.append(hunter.get_position())
      x,y = hunter.get_position()
      self.positions[x][y] = 1
        
    #After the hunters have moved, check if they caught a prey
    self.check_alive(new_hunter_pos)


    #Determine the new x,y values for the prey, store them and visually update the board
    new_prey_pos = []
    for p in self.prey:
      #Change the old locations to empty
      x,y = p.get_position()
      self.positions[x][y] = 0
      #Move and get the new locations
      p.set_postion(p.move(self.hunters, new_prey_pos))
      new_prey_pos.append(p.get_position())
      # new_prey_pos.append(p.move(self.hunters, new_prey_pos))
      x,y = new_prey_pos[-1]
      self.positions[x][y] = 2

    #Update the actual x,y values of the hunters and prey
    for i in range(len(self.hunters)):
      self.hunters[i].set_postion(new_hunter_pos[i])
      # self.check_alive()
    for i in range(len(self.prey)):
      self.prey[i].set_postion(new_prey_pos[i])

     

  #Check for each prey if it is in the same position as a hunter
  #If so, remove the prey from the board (its eaten) and reward the hunter
  def check_alive(self, new_hunter_pos):
    eaten_prey = []
    for p in self.prey:
      hunter = 0
      for (x,y) in new_hunter_pos:
        if((x,y) == p.get_position()):
          eaten_prey.append(p)
          self.hunters[hunter].feed()
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