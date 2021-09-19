import numpy as np
from hunter import Hunter
from prey import Prey
import itertools

class Board:
  def __init__(self):
    #Board is filled with values 0,1,2 for empty, hunter and prey respectively
    #Use the symbols when visualizing the board
    self.symbols = [' | | ', ' |H| ', ' |p| ']

    self.positions = [ [0] * 25 for i in range(25)]


    #Initiate the hunters  
    self.hunters = []
    # for i in range(2):
    #   self.hunters.append(Hunter())
    # self.hunters.append(Hunter((1,1)))
    self.hunters.append(Hunter((23,23)))
    #Initiate the prey 
    self.prey = []
    self.prey.append(Prey((0,0)))
    self.prey.append(Prey((0,1)))
    # for i in range(1):
    #   self.prey.append(Prey())


  def init_board(self):
    for hunter in self.hunters:
      x,y = hunter.getPosition()
      self.positions[x][y] = 1

    for p in self.prey:
      x,y = p.getPosition()
      self.positions[x][y] = 2


  def print_board(self):
    #Print the list in this order to get a 25x25 grid with [0][0] being bottom left and [24][24] top right
    for j in range(len(self.positions)-1, -1,-1):
      for i in range(len(self.positions)):
        print(self.symbols[self.positions[i][j]], end='')
      print('\n')

  def update_board(self):
    
    #Determine the new x,y values for the hunters, store them and visually update the board
    new_Hunter_Pos = []
    for hunter in self.hunters:
      #Change the old locations to empty
      x,y = hunter.getPosition()
      self.positions[x][y] = 0
      #Move and get the new locations, hunter moves twice as it is faster
      hunter.setPostion(hunter.move(self.prey, new_Hunter_Pos))
      new_Hunter_Pos.append(hunter.move(self.prey, new_Hunter_Pos))
      x,y = new_Hunter_Pos[-1]
      self.positions[x][y] = 1
      
    #After the hunters have moved, check if they caught a prey
    self.check_alive(new_Hunter_Pos)


    #Determine the new x,y values for the prey, store them and visually update the board
    new_Prey_Pos = []
    for p in self.prey:
      #Change the old locations to empty
      x,y = p.getPosition()
      self.positions[x][y] = 0
      #Move and get the new locations
      new_Prey_Pos.append(p.move(self.hunters, new_Prey_Pos))
      x,y = new_Prey_Pos[-1]
      self.positions[x][y] = 2

    #Update the actual x,y values of the hunters and prey
    for i in range(len(self.hunters)):
      self.hunters[i].setPostion(new_Hunter_Pos[i])
      # self.check_alive()
    for i in range(len(self.prey)):
      self.prey[i].setPostion(new_Prey_Pos[i])

     

  #Check for each prey if it is in the same position as a hunter
  #If so, remove the prey from the board (its eaten) and reward the hunter
  def check_alive(self, new_Hunter_Pos):
    eaten_prey = []
    for p in self.prey:
      for (x,y) in new_Hunter_Pos:
        if((x,y) == p.getPosition()):
          eaten_prey.append(p)
          break
    for eaten_p in eaten_prey:
      self.prey.remove(eaten_p)

