import numpy as np

from random import seed, choice
from os import urandom
from time import time
from itertools import cycle
from sys import argv
from TTTBoard import TTTBoard

def getTrainingData(noOfGames, dataGenFlag, inpTrainFile, outTrainFile):

    # Final Stats
    xWins = 0
    oWins = 0
    draws = 0

    # Per-Game Stats (Non-Final)
    xWinTurns = 0
    oWinTurns = 0
    drawTurns = 0

    xWinwStateSums = 0
    oWinwStateSums = 0
    drawwStateSums = 0

    # For Accepted Games (NN to be trained for X Player, i.e. takes first turn)
    totalAcceptedGames = 0
    totalAcceptedTurns = 0       # i.e. total no. of samples

    # Holds all the accepted games' data
    inpTrainList = []
    outTrainList = []

    for i in range(noOfGames):

        # print(f"Game No.: {i}")
        emptyPositions = list(range(1, 10))

        # Holds the current game's data
        inpTrainBuffer = []
        outinpTrainBuffer = []

        boardList = b.board.tolist()
        boardList.pop(0)
        inpTrainBuffer.append(boardList)

        while b.board[0] < 10:
            if b.board[0] > 4:
                status, wSindex = b.winnerCheck()
                if status == 0:
                    # print(f"Game Draw!\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    draws += 1
                    drawTurns += b.board[0]
                    drawwStateSums += b.getwStateSum()
                    if dataGenFlag == 2:
                        if b.board[0] == 9:
                            inpTrainBuffer.pop()
                            inpTrainList.extend(inpTrainBuffer)
                            outTrainList.extend(outinpTrainBuffer)
                            totalAcceptedGames += 1
                            totalAcceptedTurns += b.board[0]
                    b.resetBoard()
                    break
                elif status == 1:
                    # print(f"Player X Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    xWins += 1
                    xWinTurns += b.board[0]
                    xWinwStateSums += b.getwStateSum()
                    if dataGenFlag == 1:
                        if b.board[0] < 6:		# and b.getwStateSum() > 16:
                            inpTrainBuffer.pop()
                            inpTrainList.extend(inpTrainBuffer)
                            outTrainList.extend(outinpTrainBuffer)
                            totalAcceptedGames += 1
                            totalAcceptedTurns += b.board[0]
                    b.resetBoard()
                    break
                elif status == 2:
                    # print(f"Player O Wins!\nwState[{wSindex}]: {b.wState[wSindex]}\nwStateSum: {b.getwStateSum()}\nTurns: {b.board[0]}\n")
                    oWins += 1
                    oWinTurns += b.board[0]
                    oWinwStateSums += b.getwStateSum()
                    b.resetBoard()
                    break

            next(playerCharToggler)             # cPChar = next(playerCharToggler)
            cPNum = next(playerNumToggler)
            position = choice(emptyPositions)
            emptyPositions.remove(position)
            # print(f"Player {cPChar}: {position}")
            b.makeMove(cPNum, position)

            zeroList = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            zeroList[position - 1] = 1
            outinpTrainBuffer.append(zeroList)
            boardList = b.board.tolist()
            boardList.pop(0)
            inpTrainBuffer.append(boardList)
            # print(f"inpTrainBuffer: {inpTrainBuffer}\noutinpTrainBuffer: {outinpTrainBuffer}")

            # b.printBoard()
            # print("")

    print(f"\nXwins: {xWins} ({xWins*100/noOfGames}%)\nMean XWin Turns: {xWinTurns/xWins if xWins != 0 else 1}\nMean XWin wStateSum: {xWinwStateSums/xWins if xWins != 0 else 1}\n")
    print(f"Owins: {oWins} ({oWins*100/noOfGames}%)\nMean OWin Turns: {oWinTurns/oWins if oWins != 0 else 1}\nMean OWin wStateSum: {oWinwStateSums/oWins if oWins != 0 else 1}\n")
    print(f"Draws: {draws} ({draws*100/noOfGames}%)\nMean Draw Turns: {drawTurns/draws if draws != 0 else 1}\nMean Draw wStateSum: {drawwStateSums/draws if draws != 0 else 1}\n")

    # print(f"TotalAcceptedGames: {totalAcceptedGames}\nTotalAcceptedTurns: {totalAcceptedTurns}\n")
    # print(f"{len(inpTrainList)} inpTrainList: {inpTrainList}\n{len(outTrainList)} outTrainList: {outTrainList}\n")

    xInpList = []
    xOutList = []
    for i in range(len(inpTrainList)):
        if i % 2 == 0:
            xInpList.append(inpTrainList[i])
            xOutList.append(outTrainList[i])

    print(f"TotalAcceptedGames: {totalAcceptedGames}\nTotalAcceptedTurns: {totalAcceptedTurns}\nxAcceptedTurns: {len(xInpList)} = {len(xOutList)}\n")

    xInpArray = np.array(xInpList)
    xOutArray = np.array(xOutList)
    np.savetxt('__data__/' + inpTrainFile, xInpArray, fmt='%d')
    np.savetxt('__data__/' + outTrainFile, xOutArray, fmt='%d')

    print(f"Files {inpTrainFile} and {outTrainFile} written.\n")

if __name__ == '__main__':

    if len(argv) != 5:
        print("Provide no. of games, dataGenFlag (1|2), inpTrainFile, outTrainFile")
    else:
        startTime = time()

        b = TTTBoard()
        playerCharToggler = cycle(['X', 'O'])               # D-Char
        playerNumToggler = cycle([3, -2])                   # D-Val
        seed(urandom(128))

        getTrainingData(int(argv[1]), int(argv[2]), argv[3], argv[4])

        print(f"Time taken: {time() - startTime}s\n")
