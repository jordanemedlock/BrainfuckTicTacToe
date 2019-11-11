import unittest
from random import shuffle, sample, randint, randrange, choice
from brainfuck import Brainfuck
import time


class Var():
  def __init__(self, start, loc, val):
    self.loc = loc
    self.val = val
    self.start = start

  def set_tape(self, tape):
    tape[self.loc] = self.val

  @property
  def diff(self):
    return self.loc - self.start

  def __repr__(self):
    return f'Var(loc={self.loc}, val={self.val})'

class BFTestCase(unittest.TestCase):

  def setUp(self):
    self.bf = Brainfuck([], 0, verbose=False, wait_time=0.0)
    self.start = time.time()

  def tearDown(self):
    self.end = time.time()
    self.elapsed = self.end - self.start
    print('{} ({}s)'.format(self.id(), self.elapsed))

  def set_vars(self, *args):
    self.bf.tape = [0 for _ in args]
    for var in args:
      var.set_tape(self.bf.tape)

  def get_vars(self, start, settings):
    locs = list(range(len(settings)))
    shuffle(locs)
    vars = []
    for i, r in enumerate(settings):
      if r:
        val = choice(r)
      else:
        val = choice(range(256))
      loc = locs[i]
      vars.append(Var(start, loc, val))
    return tuple(vars)

  def make_vars(self, settings):
    start = randrange(len(settings))
    args = self.get_vars(start, settings)
    self.set_vars(*args)
    return args, start


  def assertTapeEquals(self, location, value):
    loc = location.loc if isinstance(location, Var) else location
    val = value.val if isinstance(value, Var) else value
    self.assertEqual(self.bf.tape[loc], val, msg='Location {} is {} not {}'.format(loc, self.bf.tape[loc], val))
  
  def assertTapeUnchanged(self, var):
    self.assertEqual(self.bf.tape[var.loc], var.val, msg='Location {} is {} not {}'.format(var.loc, self.bf.tape[var.loc], var.val))
