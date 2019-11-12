from random import randint
from asciimatics.screen import Screen
from brainfuck_it import Brainfuck
# from metabf import *
from tictactoe import validate_row
import time

def print_program(screen, program, index, num_lines=20):
  for i, line in enumerate(program):
    if index < len(line):
      x = index
      y = i
    elif index == len(line):
      x = None
      y = i
    else:
      index -= len(line) + 1

  start_line = max(0, int(y-num_lines/2))
  end_line = min(len(program), start_line + num_lines)

  lines = program[start_line:end_line]

  new_y = y - start_line
  for j, line in enumerate(lines):
    for i, c in enumerate(line):
      if i == x and j == y:
        colour = 1
      else:
        colour = 0
      screen.print_at(c, i, j, bg=colour)




def main(screen):

  tape = [0,0,0, 0,0,0, 0,0,0, 0,0,0,0,0]

  program = validate_row(0, 9, 10, 11, 12, 13)

  bf = Brainfuck(tape, 0, verbose=False)
  bf.setup(program)

  lines = bf.program.split('\n')
  while True:
    print_program(screen, lines, bf.counter)


    ev = screen.get_event()
    if ev in (ord('Q'), ord('q')):
      return
    if ev in (ord('p'),ord('P')):
      bf.step()


    print('refreshing screen')
    screen.refresh()


Screen.wrapper(main)