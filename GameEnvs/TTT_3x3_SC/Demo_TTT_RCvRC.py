from random import seed, choice
from os import urandom
from time import time
from itertools import cycle
from TTTBoard import TTTBoard

if __name__ == '__main__':

    startTime = time()

    b = TTTBoard()
    emptyPositions = list(range(1, 10))
    playerCharToggler = cycle(['X', 'O'])               # D-Char
    playerNumToggler = cycle([3, -2])                   # D-Val
    seed(urandom(128))

    while b.board[0] < 10:
        if b.board[0] > 4:
            status, wSindex = b.winnerCheck()
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
        position = choice(emptyPositions)
        emptyPositions.remove(position)
        print(f"\nPlayer {cPChar}: {position}")
        b.makeMove(cPNum, position)
        
        b.printBoard()
        print("")
    
    print(f"Time taken: {time() - startTime}s\n")