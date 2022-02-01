import argparse
from ast import arg
from itertools import cycle
from random import choices
from time import time
from sys import argv
from C4Board import C4Board
from C4_MCTSAgent import C4_MCTSAgent

def main(noOfGames, agentMaxIter):
	
	b = C4Board()
	b.printInfo()

	playerNumToggler = cycle([-1, 1])					# D-Val
	playerCharToggler = cycle(['O', 'X'])               # D-Char

	for i in range(noOfGames):
		agent = C4_MCTSAgent(b, 'O', -1, maxIter=agentMaxIter, verbose=False)
		while b.moveCount < 43:
			if b.moveCount > 6:
				status = b.checkWin()
				if status == 0:
					print(f"Game Draw! at move: {b.moveCount}\n")
					break
				elif status == -1:
					print(f"Player O (Human) Wins! at move: {b.moveCount}\n")
					break
				elif status == 1:
					print(f"Player X (AI) Wins! at move: {b.moveCount}\n")
					break
			cPChar = next(playerCharToggler)
			cPNum = next(playerNumToggler)
			position = None
			# Player X's turn, Agent
			if cPNum == 1:
				startTime = time()
				print("AI's turn...")
				position = agent.getMove()
				print(f"AI Chose Position: {position + 1}")
				print(f"Time taken by AI: {time() - startTime}s\n")
				print(f"\n{b.moveCount + 1}: Player {cPChar}: {position + 1}", end='', flush=True)
				b.makeMove(cPNum, position)
			# Player O's turn, Human
			elif cPNum == -1:
				print(f"\n{b.moveCount + 1}: Player {cPChar}: ", end='', flush=True)
				position = int(input()) - 1
				while not b.makeMove(cPNum, position):
					print("Already Occuipied or Invalid Position", end='')
					position = int(input()) - 1
					print(f"\n{b.moveCount + 1}: Player {cPChar}: ", end='', flush=True)
			agent.setNodeMove(cPNum, position)
			b.printBoard()
			print("")
		
		b.resetBoard()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Connect4 Human vs AI (Monte Carlo Tree Search)')
	parser.add_argument('--games', '-n', type=int, default=1, metavar='N',help='Number of games you want to play with the AI')
	parser.add_argument('--ai-difficulty', '-d', default='normal', choices=['easy', 'normal', 'hard', 'overlord'], help='Change difficulty of AI')
	args = parser.parse_args()
	if(args.ai_difficulty == 'easy'): agentMaxIter = 500
	elif(args.ai_difficulty == 'normal'): agentMaxIter = 2500
	elif(args.ai_difficulty == 'hard'): agentMaxIter = 7000
	elif(args.ai_difficulty == 'overlord'): agentMaxIter = 25000
	print(f"AI-Level set: {args.ai_difficulty}")
	main(args.games, agentMaxIter)