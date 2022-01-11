from itertools import cycle
from random import seed, choice
from os import urandom
from time import time
from C4Board import C4Board 
from sys import argv
import matplotlib.pyplot as plt

def main(noOfGames):
	
	startTime = time()
	
	b = C4Board()
	playerNumToggler = cycle([3, -2])				# D-Val
	playerCharToggler = cycle(['X', 'O'])		  	# D-Char

	# b.printInfo()

	xWins, xWinsPrev, xWinsPlot = 0, 0, []
	oWins, oWinsPrev, oWinsPlot = 0, 0, []
	draws, drawsPrev, drawsPlot = 0, 0, []
	gameNoPlot = []

	for i in range(noOfGames):
		emptyPositions = [0, 1, 2, 3, 4, 5, 6]
		# print(f"Game No.: {i + 1}")
		while b.count < 42:
			if b.count > 7:
				status, wSindex = b.checkWin()
				if status == 0:
					# print(f"Game Draw! {b.getwStateSum()}\n")
					draws += 1
					break
				elif status == 1:
					# print(f"Player X Wins! (wState[{wSindex}]: {b.wState[wSindex]}) {b.getwStateSum()}\n")
					xWins += 1
					break
				elif status == 2:
					# print(f"Player O Wins! (wState[{wSindex}]: {b.wState[wSindex]}) {b.getwStateSum()}\n")
					oWins += 1
					break

			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			position = choice(emptyPositions)
			# print(f"\nPlayer {cPChar}: {position}")
			b.makeMove(cPNum, position)

			# b.printBoard()
			# print("")
		if (i + 1) % 1000 == 0:
			print(f"Game No.: {i + 1}")
			gameNoPlot.append(i + 1)
			xWinsPlot.append((xWins - xWinsPrev) / 1000)
			oWinsPlot.append((oWins - oWinsPrev) / 1000)
			drawsPlot.append((draws - drawsPrev) / 1000)
			xWinsPrev = xWins
			oWinsPrev = oWins
			drawsPrev = draws
		b.resetBoard()

	print(f"Time taken: {time() - startTime}s\n")
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
	main(noOfGames)