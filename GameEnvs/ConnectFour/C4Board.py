from array import array
import sys

class C4Board:
	# Horizontal, Vertical, Left Diag (/), Right Diag (\)
	winCheckDict = {
		0: ((0, 1, 2, 3), (0, 7, 14, 21), (0, 8, 16, 24)),
		1: ((0, 1, 2, 3), (1, 2, 3, 4), (1, 8, 15, 22), (1, 9, 17, 25)),
		2: ((0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (2, 9, 16, 23), (2, 10, 18, 26)),
		3: ((0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (3, 10, 17, 24), (3, 9, 15, 21), (3, 11, 19, 27)),
		4: ((1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 11, 18, 25), (4, 10, 16, 22)),
		5: ((2, 3, 4, 5), (3, 4, 5, 6), (5, 12, 19, 26), (5, 11, 17, 23)),
		6: ((3, 4, 5, 6), (6, 13, 20, 27), (6, 12, 18, 24)),

		7: ((7, 8, 9, 10), (7, 14, 21, 28), (7, 15, 23, 31)),
		8: ((7, 8, 9, 10), (8, 9, 10, 11), (8, 15, 22, 29), (8, 16, 24, 32)),
		9: ((7, 8, 9, 10), (8, 9, 10, 11), (9, 10, 11, 12), (9, 16, 23, 30), (3, 9, 15, 21), (1, 9, 17, 25), (9, 17, 25, 33)),
		10: ((7, 8, 9, 10), (8, 9, 10, 11), (9, 10, 11, 12), (10, 11, 12, 13), (10, 17, 24, 31), (4, 10, 16, 22), (10, 16, 22, 28), (2, 10, 18, 26), (10, 18, 26, 34)),
		11: ((8, 9, 10, 11), (9, 10, 11, 12), (10, 11, 12, 13), (11, 18, 25, 32), (5, 11, 17, 23), (11, 17, 23, 29), (3, 11, 19, 27)),
		12: ((9, 10, 11, 12), (10, 11, 12, 13), (12, 19, 26, 33), (6, 12, 18, 24), (12, 18, 24, 30)),
		13: ((10, 11, 12, 13), (13, 20, 27, 34), (13, 19, 25, 31)),

		14: ((14, 15, 16, 17), (14, 21, 28, 35), (14, 22, 30, 38)),
		15: ((14, 15, 16, 17), (15, 16, 17, 18), (15, 22, 29, 36), (3, 9, 15, 21), (7, 15, 23, 31), (15, 23, 31, 39)),
		16: ((14, 15, 16, 17), (15, 16, 17, 18), (16, 17, 18, 19), (16, 23, 30, 37), (4, 10, 16, 22), (10, 16, 22, 28), (0, 8, 16, 24), (8, 16, 24, 32), (16, 24, 32, 40)),
		17: ((14, 15, 16, 17), (15, 16, 17, 18), (16, 17, 18, 19), (17, 18, 19, 20), (17, 24, 31, 38), (5, 11, 17, 23), (11, 17, 23, 29), (17, 23, 29, 35), (1, 9, 17, 25), (9, 17, 25, 33), (17, 25, 33, 41)),
		18: ((15, 16, 17, 18), (16, 17, 18, 19), (17, 18, 19, 20), (18, 25, 32, 39), (6, 12, 18, 24), (12, 18, 24, 30), (18, 24, 30, 36), (2, 10, 18, 26), (10, 18, 26, 34)),
		19: ((16, 17, 18, 19), (17, 18, 19, 20), (19, 26, 33, 40), (13, 19, 25, 31), (19, 25, 31, 37), (3, 11, 19, 27)),
		20: ((17, 18, 19, 20), (20, 27, 34, 41), (20, 26, 32, 38)),

		21: ((21, 22, 23, 24), (3, 9, 15, 21)),
		22: ((21, 22, 23, 24), (22, 23, 24, 25), (4, 10, 16, 22), (10, 16, 22, 28), (14, 22, 30, 38)),
		23: ((21, 22, 23, 24), (22, 23, 24, 25), (23, 24, 25, 26), (5, 11, 17, 23), (11, 17, 23, 29), (17, 23, 29, 35), (7, 15, 23, 31), (15, 23, 31, 39)),
		24: ((21, 22, 23, 24), (22, 23, 24, 25), (23, 24, 25, 26), (24, 25, 26, 27), (6, 12, 18, 24), (12, 18, 24, 30), (18, 24, 30, 36), (0, 8, 16, 24), (8, 16, 24, 32), (16, 24, 32, 40)),
		25: ((22, 23, 24, 25), (23, 24, 25, 26), (24, 25, 26, 27), (13, 19, 25, 31), (19, 25, 31, 37), (1, 9, 17, 25), (9, 17, 25, 33), (17, 25, 33, 41)),
		26: ((23, 24, 25, 26), (24, 25, 26, 27), (20, 26, 32, 38), (2, 10, 18, 26), (10, 18, 26, 34)),
		27: ((24, 25, 26, 27), (3, 11, 19, 27)),

		28: ((28, 29, 30, 31), (10, 16, 22, 28)),
		29: ((28, 29, 30, 31), (29, 30, 31, 32), (11, 17, 23, 29), (17, 23, 29, 35)),
		30: ((28, 29, 30, 31), (29, 30, 31, 32), (30, 31, 32, 33), (12, 18, 24, 30), (18, 24, 30, 36), (14, 22, 30, 38)),
		31: ((28, 29, 30, 31), (29, 30, 31, 32), (30, 31, 32, 33), (31, 32, 33, 34), (13, 19, 25, 31), (19, 25, 31, 37), (7, 15, 23, 31), (15, 23, 31, 39)),
		32: ((29, 30, 31, 32), (30, 31, 32, 33), (31, 32, 33, 34), (20, 26, 32, 38), (8, 16, 24, 32), (16, 24, 32, 40)),
		33: ((30, 31, 32, 33), (31, 32, 33, 34), (9, 17, 25, 33), (17, 25, 33, 41)),
		34: ((31, 32, 33, 34), (10, 18, 26, 34)),

		35: ((35, 36, 37, 38), (17, 23, 29, 35)),
		36: ((35, 36, 37, 38), (36, 37, 38, 39), (18, 24, 30, 36)),
		37: ((35, 36, 37, 38), (36, 37, 38, 39), (37, 38, 39, 40), (19, 25, 31, 37)),
		38: ((35, 36, 37, 38), (36, 37, 38, 39), (37, 38, 39, 40), (38, 39, 40, 41), (20, 26, 32, 38), (14, 22, 30, 38)),
		39: ((36, 37, 38, 39), (37, 38, 39, 40), (38, 39, 40, 41), (15, 23, 31, 39)),
		40: ((37, 38, 39, 40), (38, 39, 40, 41), (16, 24, 32, 40)),
		41: ((38, 39, 40, 41), (17, 25, 33, 41))
	}
	
	def __init__(self, board: array = array('i', [0] * 42)) -> None:
		self.board = board
		self.moveCount = 0
		self.lastPlayedPosition = None
		self.lastPlayerNum = -1
	
	def printBoard(self):
		pBoard = [' '] * 42
		for i in range(0, 42):
			if self.board[i] == 0:              # D-Val
				pBoard[i] = ' '
			elif self.board[i] == -1:           # D-Val
				pBoard[i] = 'O'                 # D-Char
			elif self.board[i] == 1:            # D-Val
				pBoard[i] = 'X'                 # D-Char
			else:
				sys.exit("Illegal number encountered on board. Exiting...")
		print("+---+---+---+---+---+---+---+")
		print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
		print("+---+---+---+---+---+---+---+")
		for i in range(42):
			if i in(6, 13, 20, 27, 34, 41):
				print(" " + pBoard[i] + " |")
			elif i in (0, 7, 14, 21, 28, 35):
				print("| " + pBoard[i] + "  ", end="")
			else:
				print(" " + pBoard[i] + "  ", end="")
		print("+---+---+---+---+---+---+---+")

	def resetBoard(self):
		self.board = array('i', [0] * 42)
		self.moveCount = 0
		self.lastPlayedPosition = None

	def makeMove(self, playerNum, position):
		if position < 0 or position > 6:
			return False
		
		if self.board[position + 35] == 0:
			self.board[position + 35] = playerNum
			self.lastPlayedPosition = position + 35
		elif self.board[position + 28] == 0:
			self.board[position + 28] = playerNum
			self.lastPlayedPosition = position + 28
		elif self.board[position + 21] == 0:
			self.board[position + 21] = playerNum
			self.lastPlayedPosition = position + 21
		elif self.board[position + 14] == 0:
			self.board[position + 14] = playerNum
			self.lastPlayedPosition = position + 14
		elif self.board[position + 7] == 0:
			self.board[position + 7] = playerNum
			self.lastPlayedPosition = position + 7
		elif self.board[position] == 0:
			self.board[position] = playerNum
			self.lastPlayedPosition = position
		else:
			return False
		
		self.moveCount += 1
		self.lastPlayerNum = playerNum
		return True

	def checkWin(self):
		# Handle KeyError? I FORSAW THEREFORE I GOD.
		if self.lastPlayedPosition is None: return None
		checkTuples = self.winCheckDict[self.lastPlayedPosition]
		for checkTuple in checkTuples:
			if self.board[checkTuple[0]] == self.board[checkTuple[1]] == self.board[checkTuple[2]] == self.board[checkTuple[3]] != 0:
				return self.board[self.lastPlayedPosition]
		
		if self.moveCount > 41:
			return 0
		return None
	
	def possibleMoves(self):
		possibleMoves = [i for i in range(7) if self.board[i] == 0]
		return possibleMoves if possibleMoves != [] else False

	def printInfo(self):
		print("\nGAME[0]: Connect-4\n")
		print("INFO[0]: The positions on the board are chosen via the column numbers, i.e.")
		print("+---+---+---+---+---+---+---+")
		print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
		print("+---+---+---+---+---+---+---+")
		for i in range(42):
			if i in(6, 13, 20, 27, 34, 41):
				print(f"   |")
			elif i in (0, 7, 14, 21, 28, 35):
				print(f"|    ", end="")
			else:
				print(f"    ", end="")
		print("+---+---+---+---+---+---+---+")
		print("INFO[1]: Player that loses, goes first the next game.")
		print("INFO[2]: Player O goes first in the first game.")
		print("INFO[3]: For sake of simplicity, Human Players are 'O' and the AI agent is 'X'\n")
