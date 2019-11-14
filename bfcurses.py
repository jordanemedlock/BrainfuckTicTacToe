from random import randint
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Widget, Layout, Divider, Button, Text, CheckBox
from asciimatics.exceptions import NextScene, StopApplication, ResizeScreenError
from brainfuck_it import Brainfuck
# from metabf import *
from tictactoe import validate_row
import time
import sys


class ProgramWidget(Widget):
  def __init__(self, program, counter):
    super(ProgramWidget, self).__init__('ProgramWidget', tab_stop=False)
    self.program = program
    self.counter = counter

  def update(self, frame_no):
    self.print_program()

  def reset(self):
    pass

  def process_event(self, event):
    return event

  def required_height(self, offset, width):
    return 20

  @property
  def value(self):
    return None


  def print_program(self):
    lines = self.program.split('\n')
    # counter = self.counter
    counter = self.counter
    highlight_x = -1
    highlight_y = -1
    for y, line in enumerate(lines):
      for x, c in enumerate(line):
        if counter == 0:
          highlight_x = x
          highlight_y = y
          break
        counter -= 1
      counter -= 1
      if counter <= 0:
        break

    start = max(0, highlight_y - 10)
    end = min(len(lines), start + 20)
    highlight_y -= start

    for y, line in enumerate(lines[start:end]):
      for x, c in enumerate(line):
        if x == highlight_x and y == highlight_y:
          colour = 0
          bg = 7
        else:
          colour = 7
          bg = 0
        self.frame.canvas.print_at(c, self._x + x, self._y + y, colour=colour, bg=bg)
        



  

class TapeWidget(Widget):
  def __init__(self, tape, head):
    super(TapeWidget, self).__init__('TapeWidget', tab_stop=False)
    self.tape = tape
    self.head = head

  def update(self, frame_no):

    start = max(0, self.head - 8)
    end = min(len(self.tape), start + 17)
    head = self.head - start

    for i, v in enumerate(self.tape[start:end]):
      if i == head:
        colour = 1
      else:
        colour = 7
      label = '{0:3d} '.format(i + start)
      border = '----'
      string = '{0:3d} '.format(v)
      delta = len(string)
      loc = self._x + delta * i

      self.frame.canvas.print_at(string, loc, self._y+1, colour=colour)
      self.frame.canvas.print_at(border, loc, self._y+2)
      self.frame.canvas.print_at(label, loc, self._y+3, colour=colour)
    

  def reset(self):
    pass

  def process_event(self, event):
    return event

  def required_height(self, offset, width):
    return 5

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

    print('initting...')
    layout = Layout([100], fill_frame=True)
    self.add_layout(layout)
    self.program_widget = ProgramWidget(self.bf.program, self.bf.counter)
    layout.add_widget(self.program_widget)
    layout.add_widget(Divider())
    self.tape_widget = TapeWidget(bf.tape, bf.head)
    layout.add_widget(self.tape_widget)
    layout.add_widget(Divider())
    layout2 = Layout([1,1,1,1])
    self.add_layout(layout2)
    self.delay_field = Text(on_change=self.delay_changed)
    self.delay_field.value = '0.1'
    layout2.add_widget(self.delay_field, 0)
    self.auto_box = CheckBox('Auto', on_change=self.auto_changed)
    self.auto_box.value = False
    layout2.add_widget(self.auto_box, 1)
    next_button = Button("Next", self.next)
    layout2.add_widget(next_button, 2)
    quit_button = Button("Exit", self.quit)
    layout2.add_widget(quit_button, 3)
    self.fix()

  def delay_changed(self):
    try:
      self.delay = float(self.delay_field.value)
    except:
      pass


  def auto_changed(self):
    self.auto = self.auto_box.value
    while self.auto:
      self.progress_program()
      self.reload_program()
      time.sleep(self.delay)


  def progress_program(self):
    if self.bf.counter < len(self.bf.program):
      looped = False
      while self.bf.program[self.bf.counter] not in '<>.,+-[]': # why is it so hard to skip the comments
        looped = True
        self.bf.step()
      if not looped:
        self.bf.step()


  def reload_program(self):
    self.tape_widget.tape = self.bf.tape
    self.tape_widget.head = self.bf.head
    self.tape_widget.update(None)
    self.program_widget.program = self.bf.program
    self.program_widget.counter = self.bf.counter
    self.program_widget.update(None)

  def next(self):
    self.progress_program()
    self.reload_program()

      # raise NextScene("Main")
    # else:
      # raise StopApplication("Program canceled")
    

  def quit(self):
    raise StopApplication("User pressed quit")




def main(screen, bf):
  scenes = [
    Scene([BFView(screen, bf)], -1, name="Main")
  ]

  screen.play(scenes)

bf = Brainfuck([0 for _ in range(20)], 0)
bf.setup("""

+++++++++++++++++++>
>
+++++++<<


[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]
""")

while True:
  try:
    Screen.wrapper(main, arguments=[bf])
    sys.exit()
  except ResizeScreenError as e:
    pass