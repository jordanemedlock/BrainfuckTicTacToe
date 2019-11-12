import time

class Brainfuck():
  def __init__(self, tape, head, verbose=True, wait_time=0.0):
    self.tape = tape
    self.head = head
    self.output = ''
    self.verbose = verbose
    self.wait_time = wait_time

  def build_brace_map(self):
    brace_stack = []
    self.bracemap = {}

    for i, c in enumerate(self.program):
      if c == '[': 
        brace_stack.append(i)
      elif c == ']':
        start = brace_stack.pop()
        self.bracemap[start] = i
        self.bracemap[i] = start

  def step(self):
    c = self.program[self.counter]

    if self.verbose:
      self.print(c)
  
    if c == '<':
      self.head -= 1
    elif c == '>':
      self.head += 1
    elif c == '+':
      self.tape[self.head] += 1
      self.tape[self.head] = self.tape[self.head] % 256
    elif c == '-':
      self.tape[self.head] -= 1
      if self.tape[self.head] < 0:
        self.tape[self.head] = 256 + self.tape[self.head]
    elif c == '.':
      self.output += chr(self.tape[self.head])
    elif c == ',':
      self.tape[self.head] = ord(getch.getch())
    elif c == '[' and self.tape[self.head] == 0:
      self.counter = self.bracemap[self.counter]
    elif c == ']' and self.tape[self.head] != 0:
      self.counter = self.bracemap[self.counter]

    self.counter += 1

  def run(self, program):
    self.program = program
    self.counter = 0

    self.build_brace_map()

    while self.counter < len(self.program):
      self.step()
      time.sleep(self.wait_time)


  def print(self, c):
    print('({}) => {} {}'.format(c, self.head, self.tape))
