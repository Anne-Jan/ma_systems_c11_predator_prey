from board import Board
import time
from params import num_runs
from params import board_vars
import os
import shutil
import csv

if __name__ == "__main__":

  os.mkdir("Results")
  for run in range(num_runs):
    board = Board(run)

    # board.print_board()
    print(run)
    alive = True
    while(alive):
      # time.sleep(1)
      alive = board.update_board()
      # board.print_board()
      # print('######################################################')


  # Add copy of param.py to results folder
  shutil.copyfile("params.py", "Results/params.py")
