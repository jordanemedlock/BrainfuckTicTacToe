import unittest
from ddt import ddt, data, file_data, unpack, idata
from random import shuffle, sample, randint, randrange
from brainfuck import Brainfuck
from metabf import *



def numbers(max=256, num=10):
  for i in range(num):
    yield randrange(max)

def index(*iterators): # list of iterators
  for xs in zip(*iterators):
    ns = list(range(len(xs)))
    shuffle(ns)
    locs = ns
    yield tuple(Var(l, x) for l, x in zip(locs, xs))

class Var():
  def __init__(self, loc, val):
    self.loc = loc
    self.val = val

  def set_tape(self, tape):
    tape[self.loc] = self.val

  def __repr__(self):
    return f'Var(loc={self.loc}, val={self.val})'

@ddt
class TestMetaBF(unittest.TestCase):

  def set_vars(self, tape, *vars):
    for var in vars:
      var.set_tape(tape)

  @idata(zip(index(numbers(max=0), numbers(), numbers(max=0), numbers()), numbers(max=4)))
  def test_cp(self, vars):
    tape = [0,0,0,0]
    (dest, src, temp, bystander), start = vars
    self.set_vars(tape, dest, src, temp, bystander)
    print('dest', dest, 'src', src, 'temp', temp, )
    print('before tape', tape)
    bf = Brainfuck(tape, start, verbose=False, wait_time=0.0)
    bf.run(cp(src.loc - start, dest.loc - start, temp.loc - start))
    print('after tape', bf.tape)
    self.assertEqual(bf.tape[dest.loc], src.val)
    self.assertEqual(bf.tape[src.loc], src.val)
    self.assertEqual(bf.tape[bystander.loc], src.val)
    

if __name__ == '__main__':
  unittest.main()
