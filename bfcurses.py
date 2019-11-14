from random import randint
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Widget, Layout, Divider, Button
from brainfuck_it import Brainfuck
# from metabf import *
from tictactoe import validate_row
import time
import sys

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

class ProgramWidget(Widget):
  def __init__(self, program, counter):
    super(ProgramWidget, self).__init__('ProgramWidget', tab_stop=False)
    self.program = program
    self.counter = counter

  def update(self, frame_no):
    self.frame.canvas.print_at('blah blah blah', self._x, self._y)

  def reset(self):
    pass

  def process_event(self, event):
    pass

  def required_height(self, offset, width):
    return 20

  @property
  def value(self):
    return None
  

class TapeWidget(Widget):
  def __init__(self, tape, head):
    super(TapeWidget, self).__init__('TapeWidget', tab_stop=False)
    self.tape = tape
    self.head = head

  def update(self, frame_no):
    for i, v in enumerate(self.tape):
      if i == self.head:
        colour = 1
      else:
        colour = 7
      string = '{0:3d} '.format(v)
      delta = len(string)
      self.frame.canvas.print_at(string, self._x + delta * i, self._y+1, colour=colour)
    

  def reset(self):
    pass

  def process_event(self, event):
    pass

  def required_height(self, offset, width):
    return 3

  @property
  def value(self):
    return None


class BFView(Frame):
  def __init__(self, screen, bf):
    super(BFView, self).__init__(screen, 
                                 screen.height * 2 // 3,
                                 screen.width * 2 // 3,
                                 on_load=self.reload_program,
                                 hover_focus=True,
                                 can_scroll=False,
                                 title="Brainfuck")

    self.bf = bf

    layout = Layout([100], fill_frame=True)
    self.add_layout(layout)
    self.program_widget = ProgramWidget(bf.program, bf.counter)
    layout.add_widget(self.program_widget)
    layout.add_widget(Divider())
    self.tape_widget = TapeWidget(bf.tape, bf.head)
    layout.add_widget(self.tape_widget)
    layout.add_widget(Divider())
    layout2 = Layout([1,1])
    self.add_layout(layout2)
    next_button = Button("Next", self.next)
    layout2.add_widget(next_button, 0)
    quit_button = Button("Exit", self.quit)
    layout2.add_widget(quit_button, 1)
    self.fix()

  def reload_program(self):
    pass

  def next(self):
    if self.bf.counter >= len(self.bf.program):
      self.bf.step()
    

  def quit(self):
    sys.exit(0)




def main(screen, bf):
  scenes = [
    Scene([BFView(screen, bf)], -1, name="Main")
  ]

  screen.play(scenes)

bf = Brainfuck([0 for _ in range(20)], 0)
bf.setup('+++>++>+ [-] < [-] < [-]')

Screen.wrapper(main, arguments=[bf])