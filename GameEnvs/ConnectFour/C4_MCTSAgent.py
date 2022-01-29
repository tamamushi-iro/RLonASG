from typing_extensions import Self
import numpy as np

class C4_MCTSAgent:
	def __init__(self, board, pChar, pNum, maxGames=20000, verbose=False) -> None:
		self.board = board
		self.pChar = pChar
		self.pNum = pNum
		self.maxGames = maxGames
		self.verbose = verbose
		self.currentNode = None
	
	def getMove(self, state):
		if self.currentNode is None:
			self.currentNode = Node(self.board.board, self.board.possibleMoves())
		
		if 

	def mcts(self):
		# Select / Tree Policy
		node = self.rootNode.select()
		print(node)
		# Expand
		node.expand(self.board.possibleMoves())
		print(node)
		# Roll-out / Simulate / Default Policy
		# Backpropagate / Backup
		pass

class Node:
	def __init__(self, state, possibleMoves, parent=None, childNodes=[]) -> None:
		# self.state = state
		self.parent = parent
		self.childNodes = childNodes
		self.wins = 0						# t totalValue? scores? win/games ratio?
		self.visits = 0						# n
		self.availableMoves = possibleMoves

	def __str__(self) -> str:
		return f"Parent: {self.parent} | Childs: {self.childNodes}\nState: {None}\nWins\\Visits: {self.wins}\\{self.visits}\nAvailable Moves: {self.availableMoves}"

	def select(self) -> Self:
		if self.childNodes == []: return self
		uctValue = lambda x: x.wins/x.visits + np.sqrt(2*np.log(self.visits)/x.visits)
		return sorted(self.childNodes, key=uctValue)[-1]

	def expand(self, possibleMoves):
		self.childNodes.append(Node('state:PlaceHolder', possibleMoves, parent=self, childNodes=[]))


# class Node:
# 	def __init__(self, board, player, parent=None):
# 		self.board = board.copy()
# 		self.parent = parent
# 		self.move = move
# 		self.untriedMoves = state.getMoves()
# 		self.childNodes = []
# 		self.wins = 0
# 		self.visits = 0
# 		self.player = state.player
		
# 	def selection(self):
# 		# return child with largest UCT value
# 		foo = lambda x: x.wins/x.visits + np.sqrt(2*np.log(self.visits)/x.visits)
# 		return sorted(self.childNodes, key=foo)[-1]
		
# 	def expand(self, move, state):
# 		# return child when move is taken
# 			# remove move from current node
# 		child = Node(move=move, parent=self, state=state)
# 		self.untriedMoves.remove(move)
# 		self.childNodes.append(child)
# 		return child

# 	def update(self, result):
# 		self.wins += result
# 		self.visits += 1
		
# def MCTS(currentState, itermax, currentNode=None, timeout=100):
# 	rootnode = Node(state=currentState)
# 	if currentNode is not None: rootnode = currentNode
	
# #    print(rootnode.wins, rootnode.visits)
# #    for child in rootnode.childNodes:
# #        print(child.move, child.wins, child.visits)
	
# 	start = time.clock()
# 	for i in range(itermax):
# 		node = rootnode
# 		state = currentState.Clone()
		
# 		# selection
# 			# keep going down the tree based on best UCT values until terminal or unexpanded node
# 		while node.untriedMoves == [] and node.childNodes != []:
# 			node = node.selection()
# 			state.move(node.move)

# 		# expand
# 		if node.untriedMoves != []:
# 			m = random.choice(node.untriedMoves)
# 			state.move(m)            
# 			node = node.expand(m, state)
		
# 		# rollout
# 		while state.getMoves():
# 			state.move(random.choice(state.getMoves()))
			
# 		# backpropagate
# 		while node is not None:
# 			node.update(state.result(node.player))
# 			node = node.parent
		
# 		duration = time.clock() - start
# 		if duration > timeout: break
		
# 	foo = lambda x: x.wins/x.visits
# 	sortedChildNodes = sorted(rootnode.childNodes, key=foo)[::-1]
# 	print("AI\'s computed winning percentages")
# 	for node in sortedChildNodes:
# 		print('Move: %s    Win Rate: %.2f%%' % (node.move+1, 100*node.wins/node.visits))
# 	print('Simulations performed: %s\n' % i)
# 	return rootnode, sortedChildNodes[0].move