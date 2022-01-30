from itertools import cycle
from time import time
from sys import argv
from C4Board import C4Board
from C4_MCTSAgent import C4_MCTSAgent

def main(noOfGames):
	
	startTime = time()
	b = C4Board()
	b.printInfo()

	playerNumToggler = cycle([1, -1])					# D-Val
	playerCharToggler = cycle(['X', 'O'])               # D-Char

	agent = C4_MCTSAgent(b, 'X', 1, verbose=False)

	for i in range(noOfGames):
		while b.moveCount < 43:
			if b.moveCount > 6:
				status = b.checkWin()
				if status == 0:
					print(f"Game Draw! at move: {b.moveCount}\n")
					break
				elif status == -1:
					print(f"Player O Wins! at move: {b.moveCount}\n")
					break
				elif status == 1:
					print(f"Player X Wins! at move: {b.moveCount}\n")
					break
			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			# Player X's turn, Agent
			if cPNum == 1:
				position = agent.getMove()
				print(f"Chosen Position: {position}")
				print(f"\n{b.moveCount + 1}: Player {cPChar}: {position + 1}", end='', flush=True)
				b.makeMove(cPNum, position)
			# Player O's turn, Human
			elif cPNum == -1:
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