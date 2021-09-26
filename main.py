from board import Board
import time

hunters = 5
prey = 20

if __name__ == "__main__":
  board = Board(num_hunters = hunters, num_prey = prey)

  board.print_board()
  print('######################################################')
  while(True):
    time.sleep(1)
    board.update_board()
    board.print_board()
    print('######################################################')
