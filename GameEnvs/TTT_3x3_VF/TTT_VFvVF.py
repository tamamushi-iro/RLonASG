from sys import argv
from itertools import cycle
import statistics
from TTTBoard import TTTBoard
from TTTAgent import Agent
import matplotlib.pyplot as plt

if __name__ == "__main__":

	if len(argv) != 2:
		noOfGames = 100
		# print(f"\nUsage: python {argv[0]} [no-of-games]\n")
	else:
		noOfGames = int(argv[1])

	b = TTTBoard()
	b.printInfo()
	playerCharToggler = cycle(['O', 'X'])				# D-Char
	playerNumToggler = cycle([1, 4])					# D-Val

	agentX = Agent('X', 4, b, verbose=True)
	agentO = Agent('O', 1, b, verbose=True)

	agentX.loadVFTable("xRCvVF")
	# agentO.loadVFTable("oRCvVF")

	# Initilize Empty State
	agentX.initializeState(tuple(b.board[1:]), b)
	agentO.initializeState(tuple(b.board[1:]), b)

	xWins = 0
	xWinsPrev = 0
	xWinsPlot = []
	oWins = 0
	oWinsPrev = 0
	oWinsPlot = []
	draws = 0
	drawsPrev = 0
	drawsPlot = []
	gameNoPlot = []

	for i in range(noOfGames):

		emptyPositions = list(range(1, 10))

		while b.board[0] < 10:
			# Winner Check
			if b.board[0] > 4:
				status = b.winnerCheck()
				if status == 0:
					print("Game Draw!")
					draws += 1
					break
				elif status == 1:
					print("Player O Won!")
					oWins += 1
					break
				elif status == 2:
					print("Player X Won!")
					xWins += 1
					break
			
			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			
			# If Player O's turn, ValueFunction.
			if cPNum == 1:
				position = agentO.makeMove(b)
				emptyPositions.remove(position)
				print(f"Player {cPChar}: {position}")
				prevState = tuple(b.board[1:])
				b.makeMove(cPNum, position)
				currState = tuple(b.board[1:])
				# Initilize new states
				agentO.initializeState(tuple(b.board[1:]), b)
				agentO.updateStateValue(prevState, currState, b)
				agentX.initializeState(tuple(b.board[1:]), b)
				agentX.updateStateValue(prevState, currState, b)
				b.printBoard()
				print()
			# If Player X's turn, ValueFuction.
			elif cPNum == 4:
				position = agentX.makeMove(b)
				emptyPositions.remove(position)
				print(f"Player {cPChar}: {position}")
				prevState = tuple(b.board[1:])
				b.makeMove(cPNum, position)
				currState = tuple(b.board[1:])
				# Initilize new states
				agentO.initializeState(tuple(b.board[1:]), b)
				agentO.updateStateValue(prevState, currState, b)
				agentX.initializeState(tuple(b.board[1:]), b)
				agentX.updateStateValue(prevState, currState, b)
				b.printBoard()
				print()
		
		if i % 100 == 0:
			print(f"\nGame No.: {i} and xstateCount: {agentX.stateCount}")
			gameNoPlot.append(i)
			xWinsPlot.append((xWins - xWinsPrev) / 100)
			oWinsPlot.append((oWins - oWinsPrev) / 100)
			drawsPlot.append((draws - drawsPrev) / 100)
			xWinsPrev = xWins
			oWinsPrev = oWins
			drawsPrev = draws

		b.resetBoard()
	
	agentX.saveVFTable("xRCvVF")
	# agentO.saveVFTable("oRCvVF")

	print(f"\nX-Win Probability: {statistics.mean(xWinsPlot)}")
	print(f"O-Win Probatility: {statistics.mean(oWinsPlot)}")
	print(f"Draws Probability: {statistics.mean(drawsPlot)}\n")

	plt.title("TD(0) Trained RL Agent vs Trained RL Agent")
	plt.ylabel('Win Probability')
	plt.plot(gameNoPlot, xWinsPlot, label="X-Win RL Agent")
	plt.plot(gameNoPlot, oWinsPlot, label="O-Win RL Agent")
	plt.plot(gameNoPlot, drawsPlot, label="Draws")

	plt.legend()
	plt.show()