from array import array

class C4Board:
	board = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	wState = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	count = 0

	def printBoard(self):
		pBoard = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
		for i in range(0, 35):
			if self.board[i] == 0:              # D-Val
				pBoard[i] = ' '
			elif self.board[i] == -2:           # D-Val
				pBoard[i] = 'O'                 # D-Char
			elif self.board[i] == 3:            # D-Val
				pBoard[i] = 'X'                 # D-Char
			else:
				sys.exit("Illegal number encountered on board. Exiting...")
		print("\n0   1    2    3    4    5    6")
		print("--+----+----+----+----+----+----+")
		for i in range(35):
			if i in(6, 13, 20, 27):
				print(pBoard[i] + " | ")
			else:
				print(pBoard[i]+" | ", end=" ")
		
		print("\n--+----+----+----+----+----+----+")

	def resetBoard(self	):
		self.board = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		self.wState = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		self.count = 0
	

	def makeMove(self, playerNum, position):
		if position < 0 or position > 6:
			return False
		
		if self.board[position + 28] == 0:
			self.board[position + 28] = playerNum
			self.count += 1
			return True

		if self.board[position + 21] == 0:
			self.board[position + 21] = playerNum
			self.count += 1
			return True
		
		if self.board[position + 14] == 0:
			self.board[position + 14] = playerNum
			self.count += 1
			return True

		if self.board[position + 7] == 0:
			self.board[position + 7] = playerNum
			self.count += 1
			return True

		if self.board[position] == 0:
			self.board[position] = playerNum
			self.count += 1
			return True

		else:
			return False

	def checkWin(self):
		# Vertical
		# for i in range(14):
		# 	self.wState[] = (self.board[i] + self.board[i+7] + self.board[i+14] + self.board[i+21])
		self.wState[0] = (self.board[0] + self.board[0+7] + self.board[0+14] + self.board[0+21])
		self.wState[1] = (self.board[1] + self.board[1+7] + self.board[1+14] + self.board[1+21])
		self.wState[2] = (self.board[2] + self.board[2+7] + self.board[2+14] + self.board[2+21])
		self.wState[3] = (self.board[3] + self.board[3+7] + self.board[3+14] + self.board[3+21])
		self.wState[4] = (self.board[4] + self.board[4+7] + self.board[4+14] + self.board[4+21])
		self.wState[5] = (self.board[5] + self.board[5+7] + self.board[5+14] + self.board[5+21])
		self.wState[6] = (self.board[6] + self.board[6+7] + self.board[6+14] + self.board[6+21])
		self.wState[7] = (self.board[7] + self.board[7+7] + self.board[7+14] + self.board[7+21])
		self.wState[8] = (self.board[8] + self.board[8+7] + self.board[8+14] + self.board[8+21])
		self.wState[9] = (self.board[9] + self.board[9+7] + self.board[9+14] + self.board[9+21])
		self.wState[10] = (self.board[10] + self.board[10+7] + self.board[10+14] + self.board[10+21])
		self.wState[11] = (self.board[11] + self.board[11+7] + self.board[11+14] + self.board[11+21])
		self.wState[12] = (self.board[12] + self.board[12+7] + self.board[12+14] + self.board[12+21])
		self.wState[13] = (self.board[13] + self.board[13+7] + self.board[13+14] + self.board[13+21])

		# Horizontal
		# for i in range(4):
		# 	self.wState[] = (self.board[i] + self.board[i+1] + self.board[i+2] + self.board[i+3])
		self.wState[14] = (self.board[0] + self.board[0+1] + self.board[0+2] + self.board[0+3])
		self.wState[15] = (self.board[1] + self.board[1+1] + self.board[1+2] + self.board[1+3])
		self.wState[16] = (self.board[2] + self.board[2+1] + self.board[2+2] + self.board[2+3])
		self.wState[17] = (self.board[3] + self.board[3+1] + self.board[3+2] + self.board[3+3])

		# for i in range(7, 11):
		# 	self.wState[] = (self.board[i] + self.board[i+1] + self.board[i+2] + self.board[i+3])
		self.wState[18] = (self.board[7] + self.board[7+1] + self.board[7+2] + self.board[7+3])
		self.wState[19] = (self.board[8] + self.board[8+1] + self.board[8+2] + self.board[8+3])
		self.wState[20] = (self.board[9] + self.board[9+1] + self.board[9+2] + self.board[9+3])
		self.wState[21] = (self.board[10] + self.board[10+1] + self.board[10+2] + self.board[10+3])


		# for i in range(14, 18):
		# 	self.wState[] = (self.board[i] + self.board[i+1] + self.board[i+2] + self.board[i+3])
		self.wState[22] = (self.board[14] + self.board[14+1] + self.board[14+2] + self.board[14+3])
		self.wState[23] = (self.board[15] + self.board[15+1] + self.board[15+2] + self.board[15+3])
		self.wState[24] = (self.board[16] + self.board[16+1] + self.board[16+2] + self.board[16+3])
		self.wState[25] = (self.board[17] + self.board[17+1] + self.board[17+2] + self.board[17+3])

		# for i in range(21, 25):
		# 	self.wState[] = (self.board[i] + self.board[i+1] + self.board[i+2] + self.board[i+3])
		self.wState[26] = (self.board[21] + self.board[21+1] + self.board[21+2] + self.board[21+3])
		self.wState[27] = (self.board[22] + self.board[22+1] + self.board[22+2] + self.board[22+3])
		self.wState[28] = (self.board[23] + self.board[23+1] + self.board[23+2] + self.board[23+3])
		self.wState[29] = (self.board[24] + self.board[24+1] + self.board[24+2] + self.board[24+3])

		# for i in range(28, 32):
		# 	self.wState[] = (self.board[i] + self.board[i+1] + self.board[i+2] + self.board[i+3])
		self.wState[30] = (self.board[28] + self.board[28+1] + self.board[28+2] + self.board[28+3])
		self.wState[31] = (self.board[29] + self.board[29+1] + self.board[29+2] + self.board[29+3])
		self.wState[32] = (self.board[30] + self.board[30+1] + self.board[30+2] + self.board[30+3])
		self.wState[33] = (self.board[31] + self.board[31+1] + self.board[31+2] + self.board[31+3])

		# # Positive diagonal
		# for i in range(4):
		# 	self.wState[] = (self.board[i] + self.board[i+8] + self.board[i+16] + self.board[i+24])
		self.wState[34] = (self.board[0] + self.board[0+8] + self.board[0+16] + self.board[0+24])
		self.wState[35] = (self.board[1] + self.board[1+8] + self.board[1+16] + self.board[1+24])
		self.wState[36] = (self.board[2] + self.board[2+8] + self.board[2+16] + self.board[2+24])
		self.wState[37] = (self.board[3] + self.board[3+8] + self.board[3+16] + self.board[3+24])

		# for i in range(7, 11):
		# 	self.wState[] = (self.board[i] + self.board[i+8] + self.board[i+16] + self.board[i+24])
		self.wState[38] = (self.board[7] + self.board[7+8] + self.board[7+16] + self.board[7+24])
		self.wState[39] = (self.board[8] + self.board[8+8] + self.board[8+16] + self.board[8+24])
		self.wState[40] = (self.board[9] + self.board[9+8] + self.board[9+16] + self.board[9+24])
		self.wState[41] = (self.board[10] + self.board[10+8] + self.board[10+16] + self.board[10+24])

		# # Negative diagonal
		# for i in range(6, 2, -1):
		# 	self.wState[] = (self.board[i] + self.board[i+6] + self.board[i+12] + self.board[i+18])
		self.wState[42] = (self.board[6] + self.board[6+6] + self.board[6+12] + self.board[6+18])
		self.wState[43] = (self.board[5] + self.board[5+6] + self.board[5+12] + self.board[5+18])
		self.wState[44] = (self.board[4] + self.board[4+6] + self.board[4+12] + self.board[4+18])
		self.wState[45] = (self.board[3] + self.board[3+6] + self.board[3+12] + self.board[3+18])

		# for i in range(13, 9, -1):
		# 	self.wState[] = (self.board[i] + self.board[i+6] + self.board[i+12] + self.board[i+18])
		self.wState[46] = (self.board[13] + self.board[13+6] + self.board[13+12] + self.board[13+18])
		self.wState[47] = (self.board[12] + self.board[12+6] + self.board[12+12] + self.board[12+18])
		self.wState[48] = (self.board[11] + self.board[11+6] + self.board[11+12] + self.board[11+18])
		self.wState[49] = (self.board[10] + self.board[10+6] + self.board[10+12] + self.board[10+18])

		for i in range(len(self.wState)):
			if self.wState[i] == 12:             # D-Val
				return (1, i)                   # D-Val
			if self.wState[i] == -8:            # D-Val
				return (2, i)                   # D-Val
		if self.count == 35:
			return (0, None)
		return (-1, None)

	def getwStateSum(self):
		wStateSum = 0
		for i in self.wState:
			wStateSum += i
		return wStateSum

	def printInfo(self):
		print("\nGAME[0]: Connect-4\n")
		print("INFO[0]: The positions on the board are controlled via the column numbers, i.e. \n0   1    2    3    4    5    6:")
		print("--+----+----+----+----+----+----+")
		for i in range(35):
			if i in(6, 13, 20, 27):
				print("  | ")
			else:
				print("  | ", end=" ")
		
		print("\n--+----+----+----+----+----+----+")
		print("INFO[1]: Player X goes first\n")

		