from random import seed, choice
from os import urandom
from time import time
from itertools import cycle
from sys import argv
from TTTBoard import TTTBoard

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

        # print(f"Game No.: {i}")
        emptyPositions = list(range(1, 10))
        # print(b.board.tolist())

        while b.board[0] < 10:
            if b.board[0] > 4:
                status, wSindex = b.winnerCheck()
                if status == 0:
                    # print(f"Game Draw!\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    draws += 1
                    drawTurns += b.board[0]
                    drawwStateSums += b.getwStateSum()
                    b.resetBoard()
                    break
                elif status == 1:
                    # print(f"Player X Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    xWins += 1
                    xWinTurns += b.board[0]
                    xWinwStateSums += b.getwStateSum()
                    # if b.board[0] < 8 and b.getwStateSum() > 16:
                        # print("DING!")
                    b.resetBoard()
                    break
                elif status == 2:
                    # print(f"Player O Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    oWins += 1
                    oWinTurns += b.board[0]
                    oWinwStateSums += b.getwStateSum()
                    b.resetBoard()
                    break
            
            cPChar = next(playerCharToggler)
            cPNum = next(playerNumToggler)
            position = choice(emptyPositions)
            emptyPositions.remove(position)
            # print(f"Player {cPChar}: {position}")
            b.makeMove(cPNum, position)
            # print(b.board.tolist())
            
            # b.printBoard()
            # print("")
    
    print(f"\nXwins: {xWins} ({xWins*100/noOfGames}%)\nMean XWin Turns: {xWinTurns/xWins if xWins != 0 else 1}\nMean XWin wStateSum: {xWinwStateSums/xWins if xWins != 0 else 1}\n")
    print(f"Owins: {oWins} ({oWins*100/noOfGames}%)\nMean OWin Turns: {oWinTurns/oWins if oWins != 0 else 1}\nMean OWin wStateSum: {oWinwStateSums/oWins if oWins != 0 else 1}\n")
    print(f"Draws: {draws} ({draws*100/noOfGames}%)\nMean Draw Turns: {drawTurns/draws if draws != 0 else 1}\nMean Draw wStateSum: {drawwStateSums/draws if draws != 0 else 1}\n")

if __name__ == '__main__':

    if len(argv) < 2:
        print("Provide no. of games.")
    else:
        startTime = time()

        b = TTTBoard()
        playerCharToggler = cycle(['X', 'O'])               # D-Char
        playerNumToggler = cycle([3, -2])                   # D-Val
        seed(urandom(128))

        getTrainingData(int(argv[1]))

        print(f"Time taken: {time() - startTime}s\n")