import numpy as np
from hunter import Hunter
from prey import Prey

class Board:
  def __init__(self):
    #Board is filled with values 0,1,2 for empty, hunter and prey respectively
    #Use the symbols when visualizing the board
    self.symbols = [' | | ', ' |H| ', ' |p| ']

    self.positions = [ [0] * 25 for i in range(25)]


    #Initiate the hunters  
    self.hunters = []
    for i in range(2):
      self.hunters.append(Hunter())

    #Initiate the prey 
    self.prey = []
    for i in range(5):
      self.prey.append(Prey())


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
    # print(self.positions)

  def update_board(self):
    #Determine the new x,y values for the hunters, store them and visually update the board
    new_Hunter_Pos = []
    for hunter in self.hunters:
      #Change the old locations to empty
      x,y = hunter.getPosition()
      self.positions[x][y] = 0
      #Move and get the new locations, hunter moves twice as it is faster
      hunter.setPostion(hunter.move(self.prey))
      new_Hunter_Pos.append(hunter.move(self.prey))
      x,y = new_Hunter_Pos[-1]
      self.positions[x][y] = 1

    #Determine the new x,y values for the prey, store them and visually update the board
    new_Prey_Pos = []
    for p in self.prey:
      #Change the old locations to empty
      x,y = p.getPosition()
      self.positions[x][y] = 0
      #Move and get the new locations
      new_Prey_Pos.append(p.move(self.hunters))
      x,y = new_Prey_Pos[-1]
      self.positions[x][y] = 2

    #Update the actual x,y values of the hunters and prey
    for i in range(len(self.hunters)):
      self.hunters[i].setPostion(new_Hunter_Pos[i])
    for i in range(len(self.prey)):
      self.prey[i].setPostion(new_Prey_Pos[i])

  #Check for each prey if it is in the same position as a hunter
  #If so, remove the prey from the board (its eaten) and reward the hunter
  def check_alive(self):
    print('lol')