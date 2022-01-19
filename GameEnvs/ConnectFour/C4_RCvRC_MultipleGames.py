from itertools import cycle
from random import seed, choice
from os import urandom
from time import time
from C4Board import C4Board 
from sys import argv
import matplotlib.pyplot as plt

def main(noOfGames, verbose=False):
	
	startTime = time()
	
	b = C4Board()
	playerNumToggler = cycle([1, -1])				# D-Val
	playerCharToggler = cycle(['X', 'O'])		  	# D-Char

	if verbose: b.printInfo()

	xWins, xWinsPrev, xWinsPlot = 0, 0, []
	oWins, oWinsPrev, oWinsPlot = 0, 0, []
	draws, drawsPrev, drawsPlot = 0, 0, []
	gameNoPlot = []
	dataStep = noOfGames / 100 if noOfGames > 100 else noOfGames / 10

	for i in range(noOfGames):
		emptyPositions = [0, 1, 2, 3, 4, 5, 6]
		if verbose: print(f"Game No.: {i + 1}")
		while b.moveCount < 43:
			if b.moveCount > 7:
				status = b.checkWin()
				if status == 0:
					if verbose: print(f"Game Draw!\n")
					draws += 1
					break
				elif status == -1:
					if verbose: print(f"Player O Wins!\n")
					oWins += 1
					break
				elif status == 1:
					if verbose: print(f"Player X Wins!\n")
					xWins += 1
					break

			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			position = choice(emptyPositions)
			if verbose: print(f"\nPlayer {cPChar}: {position + 1}")
			while not b.makeMove(cPNum, position):
				emptyPositions.remove(position)
				if verbose: print(f"Invalid position {position + 1}. Rechoosing from {[p + 1 for p in emptyPositions]}")
				position = choice(emptyPositions)
				if verbose: print(f"Player {cPChar}: {position + 1}")

			if verbose: b.printBoard()
			if verbose: print("")
		if (i + 1) % dataStep == 0:
			print(f"Game No.: {i + 1}")
			gameNoPlot.append(i + 1)
			xWinsPlot.append((xWins - xWinsPrev) / dataStep)
			oWinsPlot.append((oWins - oWinsPrev) / dataStep)
			drawsPlot.append((draws - drawsPrev) / dataStep)
			xWinsPrev = xWins
			oWinsPrev = oWins
			drawsPrev = draws
		b.resetBoard()

	print(f"\nTime taken: {time() - startTime}s")
	print(f"\nX-Win Probability: {xWins/noOfGames}")
	print(f"O-Win Probatility: {oWins/noOfGames}")
	print(f"Draws Probability: {draws/noOfGames}\n")

	plt.title("Random Agent vs Random Agent")
	plt.ylabel('Win Probability')
	plt.plot(gameNoPlot, xWinsPlot, label="X-Win Random")
	plt.plot(gameNoPlot, oWinsPlot, label="O-Win Random")
	plt.plot(gameNoPlot, drawsPlot, label="Draws")

	plt.legend()
	plt.show()

if __name__ == "__main__":
	if len(argv) != 2:
		noOfGames = 100
	else:
		noOfGames = int(argv[1])
	seed(urandom(128))
	main(noOfGames, verbose=False)