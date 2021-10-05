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
      # time.sleep(0.001)
      alive = board.update_board()
      # board.print_board()
      # print('######################################################')


  ### Average the results of all the runs
  averages = []
  for i in range (board_vars['max_iterations']):
    averages.append([0,0])
  print(averages)
  # First, add up all results
  for run in range(num_runs):
    with open("Results/Run" + str(run) + ".csv") as read_obj:
      csv_reader = csv.reader(read_obj)
      iterator = 0
      for line in csv_reader:
        
        averages[iterator][0] += float(line[0])
        averages[iterator][1] += float(line[1])
        iterator += 1

  # Then divide by num_runs
  for iteration in range(board_vars['max_iterations']):
    averages[iteration][0] /= num_runs
    averages[iteration][1] /= num_runs
    
  with open("Results/Averaged_Runs.csv", "w+") as my_csv:
        cs_writer = csv.writer(my_csv, delimiter=',')
        cs_writer.writerows(averages)

  # Add copy of param.py to results folder
  shutil.copyfile("params.py", "Results/params.py")
