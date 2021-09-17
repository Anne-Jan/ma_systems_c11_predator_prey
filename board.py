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
    for i in range(3):
      self.hunters.append(Hunter())

    #Initiate the prey 
    self.prey = []
    for i in range(6):
      self.prey.append(Prey())


  def init_board(self):
    print('test')
    for hunter in self.hunters:
      x = hunter.getPosition()[0]
      y = hunter.getPosition()[1]
      self.positions[x][y] = 1

    for p in self.prey:
      x = p.getPosition()[0]
      y = p.getPosition()[1]
      self.positions[x][y] = 2


  def print_board(self):
    #Print the list in this order to get a 25x25 grid with [0][0] being bottom left and [24][24] top right
    for j in range(len(self.positions)-1, -1,-1):
      for i in range(len(self.positions)):
        print(self.symbols[self.positions[i][j]], end='')
      print('\n')
    # print(self.positions)

  def update_board(self):
    for hunter in self.hunters:
      #Change the old locations to empty
      x = hunter.getPosition()[0]
      y = hunter.getPosition()[1]
      self.positions[x][y] = 0
      #Move and get the new locations
      hunter.move()
      x = hunter.getPosition()[0]
      y = hunter.getPosition()[1]
      self.positions[x][y] = 1
    for p in self.prey:
      #Change the old locations to empty
      x = p.getPosition()[0]
      y = p.getPosition()[1]
      self.positions[x][y] = 0
      #Move and get the new locations
      p.move()
      x = p.getPosition()[0]
      y = p.getPosition()[1]
      self.positions[x][y] = 2