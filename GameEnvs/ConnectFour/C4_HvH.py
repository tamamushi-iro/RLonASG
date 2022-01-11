from itertools import cycle
from time import time
from C4Board import C4Board 

if __name__=="__main__":
	
	startTime = time()

	playerNumToggler = cycle([1, -1])					# D-Val
	playerCharToggler = cycle(['X', 'O'])               # D-Char
	b = C4Board()
	b.printInfo()
	
	emptyPositions = [0, 1, 2, 3, 4, 5, 6]

	while b.count < 42:
		if b.count > 7:
			status = b.checkWin()
			if status == 0:
				print("Game Draw!\n")
				break
			elif status == -1:
				print(f"Player O Wins!\n")
				break
			elif status == 1:
				print(f"Player X Wins!\n")
				break
		cPChar = next(playerCharToggler)
		cPNum = next(playerNumToggler)
		print(f"\nPlayer {cPChar}: ", end='', flush=True)
		while not b.makeMove(cPNum, int(input()) - 1):
			print("Already Occuipied or Invalid Position", end='')
			print(f"\nPlayer {cPChar}: ", end='', flush=True)
		
		b.printBoard()
		print("")

	print(f"Time taken: {time() - startTime}s\n")