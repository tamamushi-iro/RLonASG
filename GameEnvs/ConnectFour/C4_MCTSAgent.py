import numpy as np
from copy import deepcopy
from random import choice
from itertools import cycle

class Node:
	def __init__(self, possibleMoves, playerNum, move=None, parent=None) -> None:
		self.move = move
		self.parent = parent
		self.childNodes = []
		self.wins = 0						# t totalValue? scores? win/games ratio?
		self.visits = 0						# n
		self.availableMoves = possibleMoves
		self.playerNum = playerNum

	def __str__(self) -> str:
		return f"Has Parent: {None if self.parent is None else 'Yes'} | No. of Childs: {len(self.childNodes)}\nValue: {'inf' if self.visits == 0 else self.wins/self.visits}\nWins/Visits: {self.wins}/{self.visits}\nAvailable Moves: {self.availableMoves}\n"

	def select(self):
		uctValue = lambda x: x.wins/x.visits + np.sqrt(2*np.log(self.visits)/x.visits)
		return sorted(self.childNodes, key=uctValue)[-1]

	def expand(self, move, playerNum, possibleMoves):
		child = Node(possibleMoves, playerNum, move=move, parent=self)
		self.availableMoves.remove(move)
		self.childNodes.append(child)
		return child
	
	def update(self, win):
		# print(f"Win: {win}")
		self.wins += win
		self.visits += 1


class C4_MCTSAgent:
	def __init__(self, board, pChar, pNum, maxIter=50000, verbose=False) -> None:
		self.board = board
		self.pChar = pChar
		self.pNum = pNum
		self.maxIter = maxIter
		self.verbose = verbose
		# self.node = None

	def getMove(self, currNode=None):
		# Prepare Vars for mcts
		# currBoardClone = deepcopy(self.board)
		
		# get move from mcts algo
		bestMove = self.mcts()

		# change board if nessesary

		return bestMove
		

	def mcts(self):
		rootNode = Node(possibleMoves=self.board.possibleMoves(), playerNum=self.board.lastPlayerNum)			# ?
		print(f"rootNode: {rootNode}")
		for i in range(self.maxIter):
			if self.verbose: print(f"Iteration: {i + 1}")
			node = rootNode
			state = deepcopy(self.board)									# Resets state to current game state
			if self.verbose: print(f"node: {node}")
			
			# Select / Tree Policy
			while node.availableMoves == [] and node.childNodes != []:
				node = node.select()
				if state.checkWin() is None: state.makeMove(-1 * node.parent.playerNum, node.move)
				if self.verbose: print(f"During Select: {state.lastPlayerNum}")
				if self.verbose: state.printBoard()


			# Expand - Done
			if node.availableMoves:
				randomMove = choice(node.availableMoves)
				if state.checkWin() is None: state.makeMove(-1 * node.playerNum, randomMove)
				if self.verbose: print(f"During Expand: {state.lastPlayerNum}")
				if self.verbose: state.printBoard()
				node = node.expand(randomMove, state.lastPlayerNum, state.possibleMoves())
				if self.verbose: print(f"childNode: {node}")

			# Roll-out / Simulate / Default Policy - Done?
			while state.checkWin() is None:
				if state.checkWin() is None: state.makeMove(-1 * state.lastPlayerNum, choice(state.possibleMoves()))
				if self.verbose: state.printBoard()
			status = state.checkWin()
			if self.verbose: print(status)

			# Backpropagate / Backup - Done?
			while node is not None:
				node.update(1 if status == self.pNum else 0)
				node = node.parent
		
		print(f"rootNode: {rootNode}")
		valueFunc = lambda x: x.wins/x.visits
		sortedChilds = sorted(rootNode.childNodes, key=valueFunc)[::-1]
		# print(sortedChilds)
		print(sortedChilds[0])
		for node in sortedChilds:
			print(f"Move: {node.move + 1}\tValue: {node.wins/node.visits}")
		return sortedChilds[0].move