from itertools import cycle
import random
from time import time
from C4Board import C4Board 
from sys import argv

if __name__ == '__main__':
	
	startTime = time()
	
	b = C4Board()
	emptyPositions = [0, 1, 2, 3, 4, 5, 6]
	playerNumToggler = cycle([3, -2])				# D-Val
	playerCharToggler = cycle(['X', 'O'])		  	# D-Char

	while b.count < 42:
		if b.count > 7:
			status, wSindex = b.checkWin()
			if status == 0:
				print(f"Game Draw! {b.getwStateSum()}\n")
				break
			elif status == 1:
				print(f"Player X Wins! (wState[{wSindex}]: {b.wState[wSindex]}) {b.getwStateSum()}\n")
				break
			elif status == 2:
				print(f"Player O Wins! (wState[{wSindex}]: {b.wState[wSindex]}) {b.getwStateSum()}\n")
				break

		cPChar = next(playerCharToggler)
		cPNum = next(playerNumToggler)
		position = random.choice(emptyPositions)
		print(f"\nPlayer {cPChar}: {position}")
		b.makeMove(cPNum, position)

		b.printBoard()
		print("")

	print(f"Time taken: {time() - startTime}s\n")

