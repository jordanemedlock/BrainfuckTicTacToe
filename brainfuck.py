import time


class Brainfuck():
  def __init__(self, tape, head, verbose=True, wait_time=0.1):
    self.tape = tape
    self.head = head
    self.verbose = verbose
    self.wait_time = wait_time
    self.num_ops = 0


  def split_by_token(self, l):
    for i, c in enumerate(l):
      if c in '[]':
        return l[:i], c, l[i+1:]
    return None, None, l
      

  def tokenize(self, clean_list):
    program = []
    right = clean_list
    while right:
      left, c, right = self.split_by_token(right)
      if c == '[':
        program += left
        bracket, right = self.tokenize(right)
        program.append(bracket)
      elif c == ']':
        program += left
        return program, right
      elif left is None:
        program += right
        return program, None
      else:
        program += left 
    return program, right

  def run(self, input_string):
    start = time.time()
    
    program, _ = self.tokenize(input_string)
    
    if self.verbose:
      print('running program: {}'.format(program))

    self.run_list(program)
    
    end = time.time()

    if self.verbose:
      print(f'Finished run in {end-start}s with {self.num_ops} operations.')

    return self.tape, self.head

  def run_list(self, program):
    for c in program:
      if isinstance(c, list):
        self.run_loop(c)
      elif c in '.,<>+-':
        self.run_once(c)
        time.sleep(self.wait_time)
      else:
        if self.verbose:
          print(c, end='')
    
  def run_loop(self, loop):
    if self.verbose:
      self.print('[')
    while self.tape[self.head] != 0:
      time.sleep(self.wait_time)
      if self.verbose:
        self.print(']')
      self.run_list(loop)
    if self.verbose:
      self.print(']')
    

  def run_once(self, c):
    self.num_ops += 1
    if self.verbose:
      self.print(c)
      
    if c == '+':
      self.tape[self.head] += 1
      self.tape[self.head] = self.tape[self.head] % 256
    elif c == '-':
      self.tape[self.head] -= 1
      if self.tape[self.head] < 0:
        self.tape[self.head] = 256 + self.tape[self.head]
    elif c == '>':
      self.head += 1
    elif c == '<':
      self.head -= 1
      if self.head < 0:
        print('too far left man!')
    elif c == '.':
      print(chr(self.tape[self.head] % 256))
    elif c == ',':
      ri = raw_input(': ')
      self.tape[self.head] = ord(ri[0])
    else:
      print('wtf unexpected character ', c)

  def print(self, c):
    print('({}) => {} {}'.format(c, self.head, self.tape))