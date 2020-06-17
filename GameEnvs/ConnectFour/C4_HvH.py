from itertools import cycle

from time import time
import random
from C4Board import C4Board 


if __name__=="__main__":
	
	startTime = time()

	playerCharToggler = cycle(['X', 'O'])               # D-Char
	playerNumToggler = cycle([3, -2])                   # D-Val
	b = C4Board()
	b.printInfo()
	
	emptyPositions = [0, 1, 2, 3, 4, 5, 6]

	while b.count < 35:
		if b.count > 7:
			status, wSindex = b.checkWin()
			if status == 0:
				print("Game Draw!\n")
				break
			elif status == 1:
				print(f"Player X Wins! (wState[{wSindex}]: {b.wState[wSindex]})\n")
				break
			elif status == 2:
				print(f"Player O Wins! (wState[{wSindex}]: {b.wState[wSindex]})\n")
				break
		cPChar = next(playerCharToggler)
		cPNum = next(playerNumToggler)
		print(f"\nPlayer {cPChar}: ", end='', flush=True)
		while not b.makeMove(cPNum, int(input())):
			print("Already Occuipied or Invalid Position", end='')
			print(f"\nPlayer {cPChar}: ", end='', flush=True)
		
		b.printBoard()
		print("")

	print(f"Time taken: {time() - startTime}s\n")