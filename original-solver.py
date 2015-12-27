#!/usr/bin/env python
from copy import deepcopy
from optparse import OptionParser
from math import sqrt
from operator import sub
from sys import exit

parser = OptionParser()
parser.add_option("-s","--start",
    type="int", dest="start",
    help="start of board solving range")
parser.add_option("-e","--end",
    type="int", dest="end",
    help="end of board solving range")
(options,args) = parser.parse_args()

if not ((options.start == 0 or options.start) and options.end):
    print "Please input a start (-s) and end (-e) in the boardlist range."
    exit(1)

def main():
    boardlist = get_boardlist()
    # global_min = [12335, [0, 1, 0, 1, 2, 3, 2, 3, 1, 4, 0, 4, 0, 3, 1, 2], (1, 3, 4, 4, 4)]
    global_min = get_current_min()
#   Solve the 100s
    i = 0
    with open('log.txt', 'a') as f:
        f.write("Board " + str(i) + ": " + str(boardlist[i]) + "\n")
    candidate = solve()
    if candidate and candidate[0] < global_min[0]:
        global_min = candidate
    print "GM: ", global_min
    print
    with open('log.txt', 'a') as f:
        f.write("Global min: " + str(global_min) + "\n\n")
    write_current_min(global_min)

def solve(board = [4,2,4,1,3,1,3,0,2,0,2,1,1,4,3,0], 
        distribution = [4,4,4,4,4]):
    reset_globals(board, distribution)
    solve_recursion(0)

    print "Finished with %s calls and %s solutions." % (call_counter, sol_counter)
    if distrib_solutions:
        best_distribution = min(distrib_solutions, key=distrib_solutions.get)
        best_solutions = distrib_solutions[best_distribution]
        with open('log.txt', 'a') as f:
            f.write("Min for this board is " + str(best_solutions))
            f.write(" with distribution " + str(best_distribution) + "\n")
        print "Min for this board is %s with distribution %s" % (best_solutions, best_distribution)
        print distrib_solutions
        return [best_solutions, deepcopy(board), best_distribution]
    else:
        with open('log.txt', 'a') as f:
            f.write("No solutions were found for this board!\n")
        print "No solutions were found for this board!"
        return None

def solve_recursion(iteration):
    global game_board, avail_space, themes, solution
    global sol_counter, call_counter
    call_counter += 1
    # Case of success
    if iteration == side_length * side_length:
        distribution = determine_distribution(game_board)
        if distribution in distrib_solutions:
            distrib_solutions[distribution] += 1
        else: distrib_solutions[distribution] = 1
        sol_counter += 1
    # Start solving
    for i in range(len(themes)):
        if themes[i] > 0:
            for y in range(side_length):
                for x in range(side_length):
                    if can_place_piece(x,y,i):
                        # Record progress
                        old_piece = game_board[y][x]
                        game_board[y][x] = i
                        avail_space[y][x] = False
                        themes[i] -= 1
                        solution.append([(x+1,y+1),i])
                        # Keep going
                        solve_recursion(iteration+1)
                        # Reset progress
                        game_board[y][x] = old_piece
                        avail_space[y][x] = True
                        themes[i] += 1
                        solution.pop()


def can_place_piece(x, y, piece):
  if not avail_space [y][x]: return False # Case of unavailable space
  if game_board [y][x] == piece: return False
  if y > 0: # Check up
      if game_board [y-1][x] == piece: return False
  if y < side_length-1: # Check down
      if game_board [y+1][x] == piece: return False
  if x > 0: # Check left
      if game_board [y][x-1] == piece: return False
  if x < side_length-1: # Check right
      if game_board [y][x+1] == piece: return False
  if x>0 and y>0: # Check NW
      if game_board [y-1][x-1] == piece: return False
  if x<side_length-1 and y>0: # Check NE
      if game_board [y-1][x+1] == piece: return False
  if x>0 and y<side_length-1: # Check SW
      if game_board [y+1][x-1] == piece: return False
  if x<side_length-1 and y<side_length-1: # Check SE
      if game_board [y+1][x+1] == piece: return False
  return True

def format_board(board):
    """Turns list into square matrix"""
    formatted_board = []
    side = int(sqrt(len(board)))
    for n in range(side):
        formatted_board.append(list(board[n*side:(n+1)*side]))
    return formatted_board

def reset_globals(board, distribution):
    """Reset global variables necessary for solve()"""
    global game_board, avail_space, themes, solution
    global sol_counter, call_counter, side_length, distrib_solutions
    game_board = format_board(board)
    side_length = len(game_board)
    avail_space = []
    for i in range(side_length):
        avail_space.append(side_length*[True])
    themes = distribution
    solution = []
    distrib_solutions = {}
    sol_counter, call_counter = 0, 0

def get_boardlist(filename="boards.txt"):
    text_file = open(filename, "r")
    boardlist = []
    for line in text_file:
        boardlist.append(eval(line))
    text_file.close()
    return boardlist

def determine_distribution(board):
    count = []
    flat_board = [item for sublist in board for item in sublist]
    for i in range(5):
        count.append(flat_board.count(i))
    return tuple(count)

def get_current_min(filename="current_min.txt"):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return eval(lines[-1])

def write_current_min(current_min, filename="current_min.txt"):
    with open(filename, 'a') as f:
        f.write(str(current_min))
        f.write("\n")

if __name__ == '__main__':
    main()
