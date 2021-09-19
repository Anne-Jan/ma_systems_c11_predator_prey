from board import Board
import time


if __name__ == "__main__":
  board = Board()

  board.init_board()
  board.print_board()
  print('######################################################')
  while(True):
    time.sleep(2)
    board.update_board()
    board.print_board()
    print('######################################################')
