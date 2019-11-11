import unittest
from ddt import ddt, data, file_data, unpack, idata
from random import shuffle
from brainfuck import Brainfuck
from metabf import *

def byte():
	for i in shuffle(list(range(256))):
		yield i




@ddt
class TestMetaBF(unittest.TestCase):
	@idata(zip(byte(), byte(), byte(), byte()))
	def test_move(self, dest, src, temp, bystander):
		tape = []
		

if __name__ == '__main__':
	unittest.main()