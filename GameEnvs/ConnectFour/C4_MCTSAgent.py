import numpy as np
from copy import deepcopy
from random import choice
from time import time

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
		return f"\nPlayer: {self.playerNum} | Move: {self.move if self.move is None else self.move + 1}\nHas Parent: {'No' if self.parent is None else 'Yes'} | No. of Childs: {len(self.childNodes)}\nValue: {'inf' if self.visits == 0 else self.wins/self.visits}\nWins/Visits: {self.wins}/{self.visits}\nAvailable Moves: {[m + 1 for m in self.availableMoves]}\n"

	def select(self):
		uctValue = lambda x: x.wins/x.visits + np.sqrt(2*np.log(self.visits)/x.visits)
		return sorted(self.childNodes, key=uctValue)[-1]

	def expand(self, move, playerNum, possibleMoves):
		child = Node(possibleMoves, playerNum, move=move, parent=self)
		self.availableMoves.remove(move)
		self.childNodes.append(child)
		return child
	
	def update(self, win):
		self.wins += win
		self.visits += 1

class C4_MCTSAgent:
	def __init__(self, board, pChar, pNum, maxIter=10000, timeout=100, verbose=False) -> None:
		self.board = board
		self.pChar = pChar
		self.pNum = pNum
		self.maxIter = maxIter
		self.verbose = verbose
		self.gameNode = Node(self.board.possibleMoves(), -1 * self.pNum)
		self.timeout = timeout
		# print(f"gameNode: {self.gameNode}")

	def setNodeMove(self, pNum, move):
		if self.verbose: print(f"\n\nbefore gameNode: {self.gameNode}")
		for childNode in self.gameNode.childNodes:
			if childNode.move == move:
				self.gameNode = childNode
				if self.verbose: print(f"after gameNode: {self.gameNode}")
				return
		if self.verbose: print(f"Should not reach here if X goes first. Can reach here if O goes first")
		self.gameNode = Node(self.board.possibleMoves(), pNum, move=move, parent=self.gameNode)

	def getMove(self):
		# Prepare Vars for mcts
		# get move from mcts algo
		# change board if nessesary
		return self.mcts()

	def mcts(self):
		rootNode = self.gameNode
		if self.verbose: print(f"before rootNode: {rootNode}")
		mctsStartTime = time()
		for i in range(self.maxIter):
			if self.verbose: print(f"Iteration: {i + 1}")
			node = rootNode
			state = deepcopy(self.board)									# Resets state to current game state
			if self.verbose: print(f"node: {node}")
			
			# Select / Tree Policy - Done
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

			# Roll-out / Simulate / Default Policy - Done
			if self.verbose: print("Rollout...")
			while state.checkWin() is None:
				if state.checkWin() is None: state.makeMove(-1 * state.lastPlayerNum, choice(state.possibleMoves()))
				if self.verbose: state.printBoard()
			status = state.checkWin()
			if self.verbose: print(f"status: {status}")

			# Backpropagate / Backup - Done
			while node is not None:
				node.update(1 if status == node.playerNum else 0)
				node = node.parent
			
			if(time() - mctsStartTime > self.timeout): break
		
		if self.verbose: print(f"after rootNode: {rootNode}")
		valueFunc = lambda x: x.wins/x.visits
		sortedChilds = sorted(rootNode.childNodes, key=valueFunc)[::-1]
		if self.verbose: print(f"bestChild: {sortedChilds[0]}")
		for node in sortedChilds:
			print(f"Move: {node.move + 1}\tWin Chance: {(node.wins/node.visits)*100:.2f}%")
		print(f"Iterations: {i + 1}")
		self.gameNode = rootNode
		return sortedChilds[0].move