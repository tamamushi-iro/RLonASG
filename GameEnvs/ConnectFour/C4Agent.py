from random import random, choice
from array import array
import pickle

class Agent:
	def __init__(self, pChar, pNum, training=True, verbose=False):
		self.pChar = pChar
		self.pNum = pNum
		self.training = training
		self.verbose = verbose