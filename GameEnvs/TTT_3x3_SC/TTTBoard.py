import sys
from array import array

# The TTT Board is and array.array of type 'signed int' that can hold the following values:
# 0 representing None
# -2 representing O                             # D-Main
# 3 representing X                              # D-Main

class TTTBoard:
    # board[0] represents turnCount, rest 9 int represents X's and O's on board.
    board = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    wState = array('i', [0, 0, 0, 0, 0, 0, 0, 0])

    # Core Game Functions
    # Here, playerNum can be either -2 or 3     # D-Val
    def makeMove(self, playerNum, position):
        if position < 1 or position > 9:
            return False
        if self.board[position] == 0:
            self.board[position] = playerNum
            self.board[0] += 1
            return True
        else:
            return False

    # Returns 1 if X Won, 2 if O Won, with their winning state (wState), and 0 if Draw.
    # Call winnerCheck only if turnCount > 4
    def winnerCheck(self):
        self.wState[0] = self.board[7] + self.board[8] + self.board[9]
        self.wState[1] = self.board[4] + self.board[5] + self.board[6]
        self.wState[2] = self.board[1] + self.board[2] + self.board[3]
        self.wState[3] = self.board[7] + self.board[4] + self.board[1]
        self.wState[4] = self.board[8] + self.board[5] + self.board[2]
        self.wState[5] = self.board[9] + self.board[6] + self.board[3]
        self.wState[6] = self.board[7] + self.board[5] + self.board[3]
        self.wState[7] = self.board[9] + self.board[5] + self.board[1]
        for i in range(len(self.wState)):
            if self.wState[i] == 9:             # D-Val
                return (1, i)                   # D-Val
            if self.wState[i] == -6:            # D-Val
                return (2, i)                   # D-Val
        if self.board[0] == 9:
            return (0, None)
        return (-1, None)

    # Environment Related Functions
    def resetBoard(self):
        self.board = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.wState = array('i', [0, 0, 0, 0, 0, 0, 0, 0])

    def getwStateSum(self):
        wStateSum = 0
        for i in self.wState:
            wStateSum += i
        return wStateSum

    # Secondary Function
    def printBoard(self):
        pBoard = [self.board[0], '', '', '', '', '', '', '', '', '']
        for i in range(1, 10):
            if self.board[i] == 0:              # D-Val
                pBoard[i] = ' '
            elif self.board[i] == -2:           # D-Val
                pBoard[i] = 'O'                 # D-Char
            elif self.board[i] == 3:            # D-Val
                pBoard[i] = 'X'                 # D-Char
            else:
                sys.exit("Illegal number encountered on board. Exiting...")
        print(f"{pBoard[0]}:")
        print(f" {pBoard[7]} | {pBoard[8]} | {pBoard[9]} ")
        print("---+---+---")
        print(f" {pBoard[4]} | {pBoard[5]} | {pBoard[6]} ")
        print("---+---+---")
        print(f" {pBoard[1]} | {pBoard[2]} | {pBoard[3]} ")
    
    # Unimportant Function
    def printInfo(self):
        print("\nGAME[0]: Tic-Tac-Toe\n")
        print("INFO[0]: The positions on the board are numbered like the Numpad, i.e.:")
        print("          7 | 8 | 9 \n         ---+---+---\n          4 | 5 | 6 \n         ---+---+---\n          1 | 2 | 3 ")
        print("INFO[1]: Player X goes first\n")