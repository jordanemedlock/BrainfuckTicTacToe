import unittest
from ddt import ddt, idata
from metabf import *
from tictactoe import *
from bftestcase import BFTestCase

@ddt
class TestTicTacToe(BFTestCase):

  def test_validate_row_empty(self):
    ret = 9
    self.bf.tape = [0,0,0, 0,0,0, 0,0,0, 0,0,0,0,0]

    program = validate_row(0, ret, 10, 11, 12, 13)
    print(program)
    self.bf.head = 0
    self.bf.verbose = True
    self.bf.run(program)
    self.assertTapeEquals(ret, 0)
    self.assertEquals(self.bf.head, 0)

if __name__ == '__main__':
  unittest.main()