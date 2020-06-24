from random import seed, choice
from os import urandom
from time import time
from sys import argv
from itertools import cycle
from TTTBoard import TTTBoard
from TTTAgent import Agent
import matplotlib.pyplot as plt

if __name__ == "__main__":

	if len(argv) != 2:
		noOfGames = 100
		# print(f"\nUsage: python {argv[0]} [no-of-games]\n")
	else:
		noOfGames = int(argv[1])

	startTime = time()
	seed(urandom(128))

	b = TTTBoard()
	playerCharToggler = cycle(['O', 'X'])				# D-Char
	playerNumToggler = cycle([1, 4])					# D-Val

	agent = Agent('X', 4, b)

	b.printInfo()

	# Initilize Empty State
	agent.initializeState(tuple(b.board[1:]), b)

	xWins = xWinsPrev = oWins = oWinsPrev = draws = drawsPrev = 0
	xWinsPlot = oWinsPlot = drawsPlot = gameNoPlot = []

	for i in range(noOfGames):

		# print(f"Game No.: {i}")
		# print(f"stateCount: {agent.stateCount}")
		emptyPositions = list(range(1, 10))

		while b.board[0] < 10:
			# Winner Check
			if b.board[0] > 4:
				status = b.winnerCheck()
				if status == 0:
					# print("Game Draw!")
					draws += 1
					break
				elif status == 1:
					# print("Player O Won!")
					oWins += 1
					break
				elif status == 2:
					# print("Player X Won!")
					xWins += 1
					break
			
			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			
			# If Player O's turn, Random.
			if cPNum == 1:
				position = choice(emptyPositions)
				emptyPositions.remove(position)
				# print(f"Player {cPChar}: {position}")
				prevState = tuple(b.board[1:])
				b.makeMove(cPNum, position)
				currState = tuple(b.board[1:])
				# Initilize new state (1st state)
				agent.initializeState(tuple(b.board[1:]), b)
				agent.updateStateValue(prevState, currState, b)
				# b.printBoard()
				# print()
			# If Player X's turn, ValueFuction.
			elif cPNum == 4:
				position = agent.makeMove(b)
				# print(f"Best Position: {position}")
				emptyPositions.remove(position)
				# print(f"Player {cPChar}: {position}")
				prevState = tuple(b.board[1:])
				b.makeMove(cPNum, position)
				currState = tuple(b.board[1:])
				agent.updateStateValue(prevState, currState, b)
				agent.initializeState(tuple(b.board[1:]), b)
				# b.printBoard()
				# print()
		
		if i % 1000 == 0:
			print(f"Game No.: {i} and stateCount: {agent.stateCount}")
			gameNoPlot.append(i)
			xWinsPlot.append((xWins - xWinsPrev) / 1000)
			oWinsPlot.append((oWins - oWinsPrev) / 1000)
			drawsPlot.append((draws - drawsPrev) / 1000)
			xWinsPrev = xWins
			oWinsPrev = oWins
			drawsPrev = draws

		b.resetBoard()
	
	agent.saveVFTable("xVFTable")

	print(f"\nTime taken: {time() - startTime} seconds")

	print(f"\nX-Win Probability: {xWins/noOfGames}")
	print(f"O-Win Probatility: {oWins/noOfGames}")
	print(f"Draws Probability: {draws/noOfGames}\n")

	plt.title("TD(0) Trained RL Agent vs Random Agent")
	plt.ylabel('Win Probability')
	plt.plot(gameNoPlot, xWinsPlot, label="X-Win RL Agent")
	plt.plot(gameNoPlot, oWinsPlot, label="O-Win Random")
	plt.plot(gameNoPlot, drawsPlot, label="Draws")

	plt.legend()
	plt.show()