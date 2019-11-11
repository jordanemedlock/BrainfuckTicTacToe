import unittest
from ddt import ddt, data, file_data, unpack, idata
from bftestcase import BFTestCase
from metabf import *
from random import shuffle, sample, randint, randrange, choice


@ddt
class TestMetaBF(BFTestCase):

  @idata(range(10))
  def test_cp(self, i):
    (dest, src, temp, bystander), start = self.make_vars([[0], None, [0], None])

    program = cp(src.diff, dest.diff, temp.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeEquals(dest, src.val)
    self.assertTapeUnchanged(src)
    self.assertTapeUnchanged(bystander)
    self.assertEqual(self.bf.head, start)

  @idata(range(10))
  def test_zero(self, i):
    (var, bystander1, bystander2), start = self.make_vars([None, None, None])

    program = zero(var.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeEquals(var, 0)
    self.assertTapeUnchanged(bystander1)
    self.assertTapeUnchanged(bystander2)
    self.assertEqual(self.bf.head, start)

  @idata(range(10))
  def test_const(self, i):
    (var, by1, by2), start = self.make_vars([None, None, None])
    val = randrange(256)

    program = const(var.diff, val)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeEquals(var, val)
    self.assertTapeUnchanged(by1)
    self.assertTapeUnchanged(by2)
    self.assertEqual(self.bf.head, start)

  @idata(range(10))
  def test_add(self, i):
    (dest, src, temp, by), start = self.make_vars([None, None, None, None])

    program = add(dest.diff, src.diff, temp.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeEquals(dest, (dest.val + src.val) % 256)
    self.assertTapeUnchanged(src)
    self.assertTapeUnchanged(by)
    self.assertEqual(self.bf.head, start)


  @idata(range(10))
  def test_sub(self, i):
    (dest, src, temp, by), start = self.make_vars([None, None, None, None])

    program = sub(dest.diff, src.diff, temp.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(src)
    self.assertTapeUnchanged(by)
    self.assertEqual(self.bf.head, start)
    res = dest.val - src.val 
    if res < 0:
      res = 256 + res
    self.assertTapeEquals(dest, res)


  @idata(range(10))
  def test_mult(self, i):
    (dest, src, temp1, temp2, by), start = self.make_vars([None, None, None, None, None])

    program = mult(dest.diff, src.diff, temp1.diff, temp2.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(src)
    self.assertTapeUnchanged(by)
    self.assertEqual(self.bf.head, start)
    self.assertTapeEquals(dest, (dest.val * src.val) % 256)



  @idata(range(10))
  def test_if_else(self, i):
    (cond, ret, temp1, temp2, by), start = self.make_vars([[0,1], None, None, None, None])
    num = randrange(256)

    program = if_else(cond.diff, const(ret.diff, num), zero(ret.diff), temp1.diff, temp2.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(cond)
    self.assertTapeUnchanged(by)
    self.assertEqual(self.bf.head, start)

    if cond.val > 0:
      self.assertTapeEquals(ret, num)
    else:
      self.assertTapeEquals(ret, 0)
    
  @idata(range(10))
  def test_if_true(self, i):
    (cond, ret, by1, by2), start = self.make_vars([[0,1], None, None, None])
    num = randrange(256)

    program = if_true(cond.diff, const(ret.diff, num))
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(by1)
    self.assertTapeUnchanged(by2)
    self.assertEqual(self.bf.head, start)

    if cond.val > 0:
      self.assertTapeEquals(ret, num)
    else:
      self.assertTapeUnchanged(ret)
    
  @idata(range(10))
  def test_if_false(self, i):
    (cond, ret, temp, by1, by2), start = self.make_vars([[0,1], None, None, None, None])
    num = randrange(256)

    program = if_false(cond.diff, const(ret.diff, num), temp.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(by1)
    self.assertTapeUnchanged(by2)
    self.assertEqual(self.bf.head, start)

    if cond.val == 0:
      self.assertTapeEquals(ret, num)
    else:
      self.assertTapeUnchanged(ret)

  @idata(range(10))
  def test_logical_not(self, i):
    (cond, temp, by1, by2), start = self.make_vars([[0,1], None, None, None])

    program = logical_not(cond.diff, temp.diff)
    self.bf.head = start
    self.bf.run(program)
    self.assertTapeUnchanged(by1)
    self.assertTapeUnchanged(by2)
    self.assertEqual(self.bf.head, start)

    if cond.val > 0:
      self.assertTapeEquals(cond, 0)
    else:
      self.assertTapeEquals(cond, 1)
    

if __name__ == '__main__':
  unittest.main()
