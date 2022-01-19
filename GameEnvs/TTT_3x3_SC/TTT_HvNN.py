# Needed for the NN
from keras.models import Sequential
from keras.initializers import RandomNormal
from keras.layers import Dense
from keras.layers import BatchNormalization
from keras.layers import Dropout
from sys import argv
import numpy as np

# Needed for the Game itself
from time import time
from itertools import cycle
from TTTBoard import TTTBoard

def loadData(inpDataFile, outDataFile):
    xInpTrainArray = np.loadtxt('__data__/' + inpDataFile, dtype=int)
    xOutTrainArray = np.loadtxt('__data__/' + outDataFile, dtype=int)
    inpDim = xInpTrainArray.shape[1]
    outDim = xOutTrainArray.shape[1]
    return xInpTrainArray, xOutTrainArray, inpDim, outDim

def modelInit(inpDim, outDim):
    model = Sequential()
    model.add(Dense(units=256, activation='relu', input_dim=inpDim, kernel_initializer=RandomNormal(mean=0.0, stddev=0.062, seed=None)))
    # model.add(BatchNormalization())
    model.add(Dropout(0.25))
    model.add(Dense(units=128, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.125))
    model.add(Dense(units=64, activation='relu'))
    # model.add(BatchNormalization())
    model.add(Dropout(0.0625))
    model.add(Dense(units=outDim, activation='softmax'))
    print(model.summary())
    return model

def modelCompile(model):
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def modelTrain(model, inpDataArray, outDataArray):
    model.fit(inpDataArray, outDataArray, batch_size=1024, epochs=10, verbose=1)
    return model

def predictNextMove(model, board, emptyPositions):
    inputList = board.tolist()
    inputList.pop(0)
    outputArr = model.predict(np.array([inputList]))
    outputList = list(outputArr[0])
    print(outputList)
    position = outputList.index(max(outputList)) + 1
    while(position not in emptyPositions):
        print(position)
        # print(outputList.pop(position - 1))               # YOU'RE TAKING INDEXES FROM A POPPING LIST
        print(outputList[position - 1])
        outputList[position - 1] = 0
        print(outputList)
        position = outputList.index(max(outputList)) + 1
    print(position)
    return position

# The Actual TTT Game
if __name__ == '__main__':

    if len(argv) != 3:
        print("\nProvide the training data files.\nUsage: python TTT_HvNN.py inpTrain.txt outTrain.txt\n")
    else:
        # Train the model
        xInpTrainArray, xOutTrainArray, inpDim, outDim = loadData(argv[1], argv[2])
        model = modelInit(inpDim, outDim)
        model = modelCompile(model)
        model = modelTrain(model, xInpTrainArray, xOutTrainArray)

        # TTT
        b = TTTBoard()
        b.printInfo()

        # Full Game Loop
        for i in range(10):
            emptyPositions = list(range(1, 10))
            playerCharToggler = cycle(['X', 'O'])               # D-Char
            playerNumToggler = cycle([3, -2])                   # D-Val

            # Each Game Loop
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

                if(cPNum == 3):
                    position = predictNextMove(model, b.board, emptyPositions)          # To-do: ? rename position to cPos ?
                    b.makeMove(cPNum, position)
                    emptyPositions.remove(position)
                    print(f"\nCPU {cPChar}: {position}")
                elif(cPNum == -2):
                    print(f"\nPlayer {cPChar}: ", end='', flush=True)
                    while True:
                        hPos = int(input())
                        if not b.makeMove(cPNum, hPos):
                            print("Already Occuipied or Invalid Position", end='')
                            print(f"\nPlayer {cPChar}: ", end='', flush=True)
                            continue
                        else:
                            emptyPositions.remove(hPos)
                            break

                b.printBoard()
                print("")
            b.resetBoard()
