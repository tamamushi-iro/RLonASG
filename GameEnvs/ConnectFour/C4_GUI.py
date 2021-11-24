import tkinter
import C4Board
from itertools import cycle

top = tkinter.Tk()
c4=C4Board.C4Board()
playerCharToggler = cycle(['X', 'O'])
playerNumToggler = cycle([3, -2]) 
#x=3=yellow
#o=-2=red
canvas = tkinter.Canvas(top, height=600, width=700)

slots=[]
for j in range(6):
    for i in range(7):
        s=canvas.create_oval((i*100)+5,(j*100)+5,(i*100)+95,(j*100)+95)
        slots.append(s)


buttons=[]
canvas.grid(column=0, row=0, columnspan=7)
for i in range(7):
    b=tkinter.Button(top, height=2, width=10, command=lambda i=i: play(i), text='Yellow')
    b.grid(column=i,row=2)
    buttons.append(b)

def buttonDisabler():
    for b in buttons:
        b.configure(state='disabled')

def play(pos):
    cPChar = next(playerCharToggler)
    cPNum = next(playerNumToggler)

    if cPNum==-2:
        for b in buttons:
            b.configure(text='Yellow')
    elif cPNum==3:
        for b in buttons:
            b.configure(text='Red')

    print(f"\nPlayer {cPChar}: ", end='', flush=True)
    if not c4.makeMove(cPNum, pos):
        print("Already Occuipied or Invalid Position", end='')
        print(f"\nPlayer {cPChar}: ", end='', flush=True)

    c4.printBoard()
    print("")

    for i in range(42):
        if c4.board[i]==-2:
            canvas.itemconfigure(slots[i], fill="red")
        elif c4.board[i]==3:
            canvas.itemconfigure(slots[i], fill="yellow")

    if c4.count>6:
        status, wSindex = c4.checkWin()
        if status == 0:
            print("Game Draw!\n")
            canvas.create_text(350,300,text="Game Draw", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()
        elif status == 1:
            print(f"Player X Wins! (wState[{wSindex}]: {c4.wState[wSindex]})\n")
            canvas.create_text(350,300,text="Yellow Won", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()
        elif status == 2:
            print(f"Player O Wins! (wState[{wSindex}]: {c4.wState[wSindex]})\n")
            canvas.create_text(350,300,text="Red Won", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()

top.mainloop()
