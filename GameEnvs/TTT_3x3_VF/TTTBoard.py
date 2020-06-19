import sys
from array import array

# The TTT Board is and array.array of type 'unsigned int' that can hold the following values:
# 0 representing None
# 1 representing O                              # D-Main
# 4 representing X                              # D-Main

class TTTBoard:
    # board[0] represents turnCount, rest 9 int represents X's and O's on board.
    board = array('I', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Core Game Functions
    # Here, playerNum can be either 1 or 4      # D-Val
    def makeMove(self, playerNum, position):
        if position < 1 or position > 9:
            return False
        if self.board[position] == 0:
            self.board[position] = playerNum
            self.board[0] += 1
            return True
        else:
            return False

    # Returns 1 if O Won, 2 if X Won, with their winning state (wState), and 0 if Draw.
    # Call winnerCheck only if turnCount > 4    # D-Main
    def winnerCheck(self):               # D-Val (s)
        if self.board[7] == self.board[8] == self.board[9] != 0:
            return 1 if self.board[7] == 1 else 2
        elif self.board[4] == self.board[5] == self.board[6] != 0:
            return 1 if self.board[4] == 1 else 2
        elif self.board[1] == self.board[2] == self.board[3] != 0:
            return 1 if self.board[1] == 1 else 2
        elif self.board[7] == self.board[4] == self.board[1] != 0:
            return 1 if self.board[7] == 1 else 2
        elif self.board[8] == self.board[5] == self.board[2] != 0:
            return 1 if self.board[8] == 1 else 2
        elif self.board[9] == self.board[6] == self.board[3] != 0:
            return 1 if self.board[9] == 1 else 2
        elif self.board[7] == self.board[5] == self.board[3] != 0:
            return 1 if self.board[7] == 1 else 2
        elif self.board[9] == self.board[5] == self.board[1] != 0:
            return 1 if self.board[9] == 1 else 2
        
        if self.board[0] == 9:
            return 0
        
    def winnerCheckState(self, stateArr):               # D-Val (s)
        if stateArr[7] == stateArr[8] == stateArr[9] != 0:
            return 1 if stateArr[7] == 1 else 2
        elif stateArr[4] == stateArr[5] == stateArr[6] != 0:
            return 1 if stateArr[4] == 1 else 2
        elif stateArr[1] == stateArr[2] == stateArr[3] != 0:
            return 1 if stateArr[1] == 1 else 2
        elif stateArr[7] == stateArr[4] == stateArr[1] != 0:
            return 1 if stateArr[7] == 1 else 2
        elif stateArr[8] == stateArr[5] == stateArr[2] != 0:
            return 1 if stateArr[8] == 1 else 2
        elif stateArr[9] == stateArr[6] == stateArr[3] != 0:
            return 1 if self.board[9] == 1 else 2
        elif stateArr[7] == stateArr[5] == stateArr[3] != 0:
            return 1 if self.board[7] == 1 else 2
        elif stateArr[9] == stateArr[5] == stateArr[1] != 0:
            return 1 if stateArr[9] == 1 else 2
        
        if stateArr[0] == 9:
            return 0

    # Get Possible States. Returns list of tuples of all possible states that could be possible from current state.
    def possibleStates(self, pNum):
        possibleStatesList = []
        positionList = []
        currBoard = self.board[1:]
        for i in range(9):
            if currBoard[i] == 0:
                currBoard[i] = pNum
                possibleStatesList.append(tuple(currBoard))
                positionList.append(i + 1)
                currBoard[i] = 0
        return possibleStatesList, positionList

    # Environment Related Functions
    def resetBoard(self):
        self.board = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Secondary Function
    def printBoard(self):
        pBoard = [self.board[0], '', '', '', '', '', '', '', '', '']
        for i in range(1, 10):
            if self.board[i] == 0:              # D-Val
                pBoard[i] = ' '
            elif self.board[i] == 1:			# D-Val
                pBoard[i] = 'O'                 # D-Char
            elif self.board[i] == 4:            # D-Val
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