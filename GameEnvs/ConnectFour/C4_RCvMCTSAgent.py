from itertools import cycle
from random import seed, choice
from os import urandom
from time import time
from C4Board import C4Board 
from sys import argv
from C4_MCTSAgent import C4_MCTSAgent
import matplotlib.pyplot as plt
import argparse

def main(noOfGames, agentMaxIter, agentTimeout, verbose=False):
	
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
		agent = C4_MCTSAgent(b, 'O', -1, maxIter=agentMaxIter, timeout=agentTimeout, verbose=False)
		emptyPositions = [0, 1, 2, 3, 4, 5, 6]
		if verbose: print(f"Game No.: {i + 1}")
		while b.moveCount < 43:
			if b.moveCount > 6:
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
			# Player X's turn, Agent
			if cPNum == 1:
				startTime = time()
				if verbose: print("AI's turn...")
				position = agent.getMove()
				if verbose: print(f"AI Chose Position: {position + 1}")
				if verbose: print(f"Time taken by AI: {(time() - startTime):.2f}s\n")
				if verbose: print(f"\n{b.moveCount + 1}: Player {cPChar}: {position + 1}", end='', flush=True)
				b.makeMove(cPNum, position)
			# Player O's turn, Random
			elif cPNum == -1:
				position = choice(emptyPositions)
			agent.setNodeMove(cPNum, position)
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

	plt.title("MCTS Agent vs Random Agent")
	plt.ylabel('Win Probability')
	plt.plot(gameNoPlot, xWinsPlot, label="X-Win MCTS Agent")
	plt.plot(gameNoPlot, oWinsPlot, label="O-Win Random Agent")
	plt.plot(gameNoPlot, drawsPlot, label="Draws")

	plt.legend()
	plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Connect4 Human vs AI (Monte Carlo Tree Search)')
	parser.add_argument('--games', '-n', type=int, default=1, metavar='N', help='Number of games you want to play with the AI')
	parser.add_argument('--ai-difficulty', '-d', default='normal', choices=['easy', 'normal', 'hard', 'overlord'], help='Change difficulty of AI')
	parser.add_argument('--ai-timeout', '-t', type=float, metavar='s', help='Max seconds the ai should spend thinking.')
	args = parser.parse_args()
	if(args.ai_difficulty == 'easy'): agentMaxIter, agentTimeout = 500, 2.5
	elif(args.ai_difficulty == 'normal'): agentMaxIter, agentTimeout = 2500, 5
	elif(args.ai_difficulty == 'hard'): agentMaxIter, agentTimeout = 7000, 7
	elif(args.ai_difficulty == 'overlord'): agentMaxIter, agentTimeout = 25000, 25
	if(args.ai_timeout): agentTimeout = args.ai_timeout
	print(f"AI-Level set: {args.ai_difficulty}")
	print(f"AI-Timeout set: {agentTimeout}")
	main(args.games, agentMaxIter, agentTimeout)