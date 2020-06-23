from array import array

class Agent:
	# Kinda? Abstract Learning/Random Agent. Could be X or O. Not Sure. NO, NOT ABSTRACT. FUNCTIONING AS X PLAYER.
	def __init__(self, pChar, pNum, training=True):
		self.stateValueTable = dict()
		self.pChar = pChar
		self.pNum = pNum
		self.training = training
		self.alpha = 0.9						# Learning-rate
		# self.epsilon = 0.1					# Exploration-factor. Unused.
		self.stateCount = 0

	def getBestPosition(self, board):
		possibleStates, positions = board.possibleStates(self.pNum)
		# Initialize all possible next/curr states
		for state in possibleStates:
			self.initializeState(state, board)
		maxValue = -100
		positionIndex = -1
		for i in range(len(possibleStates)):
			if self.stateValueTable[possibleStates[i]] > maxValue:
				print(f"{possibleStates[i]}: {self.stateValueTable[possibleStates[i]]}")
				maxValue = self.stateValueTable[possibleStates[i]]
				positionIndex = i
		return positions[positionIndex]

	def initializeState(self, state, board):
		if state not in self.stateValueTable:
			self.stateValueTable[state] = self.initialStateValues(board, state)
			self.stateCount += 1

	def updateStateValue(self, prevState, currState, board):
		if self.training:
			self.stateValueTable[prevState] += self.alpha * (self.stateValueTable[currState] - self.stateValueTable[prevState])
			print(f"Updated prevState {prevState}: {self.stateValueTable[prevState]} using currState {currState}: {self.stateValueTable[currState]}")

	def initialStateValues(self, board, state):
		stateList = list(state)
		stateList.insert(0, board.board[0] + 1)
		stateArr = array('I', stateList)
		status = board.winnerCheckState(stateArr)
		# print(f"initialStateValues board: {stateArr}")
		# print(f"initialStateValues status: {status}")
		if status == 0:
			return 1
		elif status == 1:
			return 0
		elif status == 2 and self.pNum == 4:
			return 1
		else:
			return 0.5