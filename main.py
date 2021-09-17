from board import Board


if __name__ == "__main__":
  board = Board()
  board.init_board()
  board.print_board()

  counter = 0
  while(True):
    counter+=1
    if counter == 10000000:
      board.update_board()
      board.print_board()
      counter = 0
      print('######################################################')
