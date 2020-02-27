from itertools import cycle
import random
import time
from C4Board import C4Board 
from sys import argv


def getTrainingData(noOfGames):

    # Final Stats
    xWins = 0
    oWins = 0
    draws = 0

    # Non-Final Stats
    xWinTurns = 0
    oWinTurns = 0
    drawTurns = 0

    xWinwStateSums = 0
    oWinwStateSums = 0
    drawwStateSums = 0

    for i in range(noOfGames):

        print(f"Game No.: {i}")
        emptyPositions = [0, 1, 2, 3, 4, 5, 6]
        
        while b.count < 35:
        	if b.count > 7:
        		status, wSindex = b.checkWin()
        		if status == 0:
        			print(f"Game Draw!\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
        			draws += 1
        			drawTurns += b.count
        			drawwStateSums += b.getwStateSum()
        			b.resetBoard()
        			break
        		elif status == 1:
        			print(f"Player X Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
        			xWins += 1
        			xWinTurns += b.count
        			xWinwStateSums += b.getwStateSum()
        			b.resetBoard()
        			break
        		elif status == 2:
	        		print(f"Player O Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
        			oWins += 1
        			oWinTurns += b.count
        			oWinwStateSums += b.getwStateSum()
        			b.resetBoard()
        			break

        	cPChar = next(playerCharToggler)
        	cPNum = next(playerNumToggler)
        	b.makeMove(cPNum, random.choice(emptyPositions))
        	
        	b.printBoard()
       	# time.sleep(1)
            
            # print("")
    print(f"\nXwins: {xWins} ({xWins*100/noOfGames}%)\nMean XWin Turns: {xWinTurns/xWins if xWins != 0 else 1}\nMean XWin wStateSum: {xWinwStateSums/xWins if xWins != 0 else 1}\n")
    print(f"Owins: {oWins} ({oWins*100/noOfGames}%)\nMean OWin Turns: {oWinTurns/oWins if oWins != 0 else 1}\nMean OWin wStateSum: {oWinwStateSums/oWins if oWins != 0 else 1}\n")
    print(f"Draws: {draws} ({draws*100/noOfGames}%)\nMean Draw Turns: {drawTurns/draws if draws != 0 else 1}\nMean Draw wStateSum: {drawwStateSums/draws if draws != 0 else 1}\n")


if __name__ == '__main__':

    if len(argv) < 2:
        print("Provide no. of games.")
    else:
        startTime = time.time()

        b = C4Board()
        playerCharToggler = cycle(['X', 'O'])               # D-Char
        playerNumToggler = cycle([3, -2])                   # D-Val

        getTrainingData(int(argv[1]))

        print(f"Time taken: {time.time() - startTime}s\n")