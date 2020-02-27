from itertools import cycle
from TTTBoard import TTTBoard

if __name__ == '__main__':
    playerCharToggler = cycle(['X', 'O'])               # D-Char
    playerNumToggler = cycle([3, -2])                   # D-Val
    b = TTTBoard()
    b.printInfo()

    while b.board[0] < 10:
        if b.board[0] > 4:
            status, wSindex = b.winnerCheck()
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