from itertools import cycle
from time import time
from sys import argv
from C4Board import C4Board

def main(noOfGames):
	
	startTime = time()

	playerNumToggler = cycle([1, -1])					# D-Val
	playerCharToggler = cycle(['X', 'O'])               # D-Char
	b = C4Board()
	b.printInfo()

	for i in range(noOfGames):
		while b.moveCount < 43:
			if b.moveCount > 6:
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
			print(f"\n{b.moveCount + 1}: Player {cPChar}: ", end='', flush=True)
			while not b.makeMove(cPNum, int(input()) - 1):
				print("Already Occuipied or Invalid Position", end='')
				print(f"\n{b.moveCount + 1}: Player {cPChar}: ", end='', flush=True)
			
			b.printBoard()
			print("")
		
		print(f"Time taken: {time() - startTime}s\n")
		b.resetBoard()

if __name__ == "__main__":
	if len(argv) != 2:
		noOfGames = 1
	else:
		noOfGames = int(argv[1])
	main(noOfGames)