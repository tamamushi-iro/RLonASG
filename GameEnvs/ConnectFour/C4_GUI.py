import tkinter
import C4Board
from itertools import cycle
from C4_MCTSAgent import C4_MCTSAgent

top = tkinter.Tk()

gameMode=tkinter.IntVar()
mb = tkinter.Menubutton(top, text="Game mode", relief=tkinter.RAISED)
mb.menu = tkinter.Menu(mb)
mb["menu"]=mb.menu
mb.menu.add_radiobutton(label="Human vs Human", variable=gameMode, value=0)
mb.menu.add_radiobutton(label="Human vs AI", variable=gameMode, value=1)
mb.grid(column=0, row=0)

gameDifficulty=tkinter.StringVar()
mb2 = tkinter.Menubutton(top, text="Game difficulty", relief=tkinter.RAISED)
mb2.menu = tkinter.Menu(mb2)
mb2["menu"]=mb2.menu
mb2.menu.add_radiobutton(label="Easy", variable=gameDifficulty, value="easy")
mb2.menu.add_radiobutton(label="Normal", variable=gameDifficulty, value="normal")
mb2.menu.add_radiobutton(label="Hard", variable=gameDifficulty, value="hard")
mb2.menu.add_radiobutton(label="Overlord", variable=gameDifficulty, value="overlord")
mb2.grid(column=1, row=0)

winnerName=None

def start():
    global agent
    if(gameDifficulty.get() == 'easy'): agentMaxIter, agentTimeout = 500, 2.5
    elif(gameDifficulty.get() == 'normal'): agentMaxIter, agentTimeout = 2500, 5
    elif(gameDifficulty.get() == 'hard'): agentMaxIter, agentTimeout = 7000, 7
    elif(gameDifficulty.get() == 'overlord'): agentMaxIter, agentTimeout = 25000, 25
    if gameMode.get(): 
        agent = C4_MCTSAgent(c4, 'X', 1, maxIter=agentMaxIter, timeout=agentTimeout, verbose=False, ui='GUI')
    if c4.moveCount: reset()
    buttonEnabler()

def reset():
    global playerCharToggler, playerNumToggler
    c4.resetBoard()
    fillCircle()
    buttonEnabler()
    print("reset")
    canvas.itemconfig(winnerName, text="")
    for b in buttons:
        b.configure(text='Red')
    playerCharToggler = cycle(['O', 'X'])
    playerNumToggler = cycle([-1, 1])
    statusText.set(gameMode.get())
    sbar.update()


mb3 = tkinter.Button(top, height=2, width=10, command=start, text='Start')
mb3.grid(column=2, row=0)

canvas = tkinter.Canvas(top, height=600, width=700)

slots=[]
for j in range(6):
    for i in range(7):
        s=canvas.create_oval((i*100)+5,(j*100)+5,(i*100)+95,(j*100)+95, fill="white")
        slots.append(s)

top.title("Connect4 - Human vs AI")
c4=C4Board.C4Board()

playerCharToggler = cycle(['O', 'X'])
playerNumToggler = cycle([-1, 1])
#x=1=yellow=AI
#o=-1=red=Human

buttons=[]
canvas.grid(column=0, row=1, columnspan=7)
for i in range(7):
    b=tkinter.Button(top, height=2, width=10, command=lambda i=i: play(i), text='Red')
    b.grid(column=i, row=2)
    buttons.append(b)

statusText = tkinter.StringVar()
statusText.set(gameMode.get())
sbar = tkinter.Label(top, textvariable=statusText, relief=tkinter.SUNKEN, anchor="w", width=100)
sbar.grid(column=0, row=3, columnspan=7)
sbar.update()

def buttonDisabler():
    for b in buttons:
        b.configure(state='disabled')

buttonDisabler()

def buttonEnabler():
    for b in buttons:
        b.configure(state='active')

def play(pos):
    global playerCharToggler, playerNumToggler
    cPChar = next(playerCharToggler)
    cPNum = next(playerNumToggler)
    
    if not gameMode.get():
        if cPNum==-1:
            for b in buttons:
                b.configure(text='Yellow')
        elif cPNum==1:
            for b in buttons:
                b.configure(text='Red')
    else:
        if cPNum==-1:
            for b in buttons:
                b.configure(text='Red')
        elif cPNum==1:
            for b in buttons:
                b.configure(text='Yellow')
    
    if not c4.makeMove(cPNum, pos):
        print("Already Occuipied or Invalid Position", end='')
        print(f"\nPlayer {cPChar}: ", flush=True)

    if not gameMode.get():
        fillCircle()
        if checkStatus(): return
    else:
        fillCircle()
        statusText.set("AI is thinking...")
        buttonDisabler()
        fillCircle()
        if checkStatus(): return
        agent.setNodeMove(-1, pos)
        agentMove()
        statusText.set(f"AI Win probability: {agent.lastWinProbability:.2f}%. Your turn...")
        buttonEnabler()
        fillCircle()
        if checkStatus(): return
    
def agentMove():
    global playerCharToggler, playerNumToggler
    position = agent.getMove()
    c4.makeMove(1, position)
    agent.setNodeMove(1, position)
    next(playerCharToggler)
    next(playerNumToggler)

def fillCircle():
    for i in range(42):
        if c4.board[i]==-1:
            canvas.itemconfigure(slots[i], fill="red")
        elif c4.board[i]==1:
            canvas.itemconfigure(slots[i], fill="yellow")
        else:
            canvas.itemconfigure(slots[i], fill="white")
    top.update()

def checkStatus():
    global winnerName
    if c4.moveCount>6:
        status = c4.checkWin()
        if status == 0:
            print("Game Draw!\n")
            statusText.set("Game Draw!")
            winnerName = canvas.create_text(350,300,text="Game Draw", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()
        elif status == -1:
            print(f"Player O Wins!\n")
            statusText.set("Player O Wins!")
            winnerName = canvas.create_text(350,300,text="Red Won", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()
        elif status == 1:
            print(f"Player X Wins!\n")
            statusText.set("Player X Wins!")
            winnerName = canvas.create_text(350,300,text="Yellow Won", fill="black", font=('Helvetica 24 bold'))
            buttonDisabler()
        top.update()
        return True if status in [0, -1, 1] else False

top.mainloop()