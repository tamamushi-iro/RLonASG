from random import random, choice
from array import array
import pickle

class Agent:
	# Kinda? Abstract Learning/Random Agent. Could be X or O. Not Sure. NO, NOT ABSTRACT. FUNCTIONING AS X PLAYER.
	# UPDATE: I think I made abstract again.
	def __init__(self, pChar, pNum, training=True, verbose=False):
		self.stateValueTable = dict()
		self.pChar = pChar
		self.pNum = pNum
		self.training = training
		self.alpha = 0.99						# Learning-rate
		self.epsilon = 0.1						# Exploration-factor
		self.stateCount = 0
		self.verbose = verbose

	def makeMove(self, board):
		possibleStates, positions = board.possibleStates(self.pNum)
		# Initialize all possible next/curr states
		for state in possibleStates:
			self.initializeState(state, board)
		if random() < self.epsilon:
			if self.verbose: print("Exploring...")
			return choice(positions)
		maxValue = -100
		positionIndex = -1
		for i in range(len(possibleStates)):
			if self.stateValueTable[possibleStates[i]] > maxValue:
				if self.verbose: print(f"[{self.pChar}]: {possibleStates[i]}: {self.stateValueTable[possibleStates[i]]}")
				maxValue = self.stateValueTable[possibleStates[i]]
				positionIndex = i
		return positions[positionIndex]

	def saveVFTable(self, fileName):
		with open("__data__/" + fileName + '.pkl', 'wb') as f:
			pickle.dump(self.stateValueTable, f, pickle.HIGHEST_PROTOCOL)
	
	def loadVFTable(self, fileName):
		with open("__data__/" + fileName + '.pkl', 'rb') as f:
			self.stateValueTable = pickle.load(f)
		self.stateCount = len(self.stateValueTable.keys())
		print(f"Loaded __data__/{fileName} with states: {self.stateCount}")

	def updateStateValue(self, prevState, currState, board):
		if self.training:
			self.stateValueTable[prevState] += self.alpha * (self.stateValueTable[currState] - self.stateValueTable[prevState])
			if self.verbose: print(f"[{self.pChar}]: Updated prevState {prevState}: {self.stateValueTable[prevState]} using currState {currState}: {self.stateValueTable[currState]}")

	def initializeState(self, state, board):
		if state not in self.stateValueTable:
			self.stateValueTable[state] = self.initialStateValues(board, state)
			self.stateCount += 1

	def initialStateValues(self, board, state):
		stateList = list(state)
		stateList.insert(0, board.board[0] + 1)
		stateArr = array('I', stateList)
		status = board.winnerCheckState(stateArr)
		# print(f"initialStateValues board: {stateArr}")
		# print(f"initialStateValues status: {status}")
		if status == 0:								# if Draw
			return 1
		elif status == 1:							# if Player O Wins
			return 1 if self.pNum == 1 else 0
		elif status == 2:							# if Player X Wins
			return 1 if self.pNum == 4 else 0
		else:
			return 0.5