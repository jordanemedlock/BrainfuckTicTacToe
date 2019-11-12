from random import randint
from asciimatics.screen import Screen
from brainfuck_it import Brainfuck
from metabf import *
from tictactoe import *

def print_program(screen, program, index, num_lines=20):
  x, y = 0, 0
  for i, c in enumerate(program):
    if y >= num_lines:
      return
    colour = 7
    if i == index:
      colour = 1
    if c == '\n':
      x = 0
      y += 1
      continue
    screen.print_at(c, x, y, colour=colour)
    x += 1


def demo(screen):

  tape = [0,0,0, 0,0,0, 0,0,0, 0,0,0,0,0]

  program = validate_row(0, 9, 10, 11, 12, 13)

  bf = Brainfuck(tape, 0)

  lines = program.split('\n')
  while True:
    print_program(screen, program, 10)

    ev = screen.get_key()
    if ev in (ord('Q'), ord('q')):
      return
    screen.refresh()

Screen.wrapper(demo)