import tkinter

from C4Board import C4Board
from itertools import cycle
from C4_MCTSAgent import C4_MCTSAgent

class C4GUIClient:
	def __init__(self):
		self.main_win = tkinter.Tk()
		self.game_mode = tkinter.StringVar(value='vs Human - Local')
		self.game_diff = tkinter.StringVar(value='easy')
		self.col_btns = []
		self.board_slots = []
		self.status_text = tkinter.StringVar(value='Enter Coin...')
		self.status_bar = tkinter.Label(self.main_win, textvariable=self.status_text, relief=tkinter.SUNKEN, anchor=tkinter.W, width=100)
		self.board_canvas = tkinter.Canvas(self.main_win, height=600, width=700)
		self.winner_text = None

		self.c4board = C4Board()
		self.mcts_agent = None
		self.playerCharToggler = cycle(['O', 'X'])
		self.playerNumToggler = cycle([-1, 1])

		### Initialise GUI
		# Main Window
		self.main_win.title('Connect4')
		self.main_win.minsize(width=708, height=710)
		self.main_win.maxsize(width=708, height=710)
		
		# Menubar
		menu_bar = tkinter.Menu(self.main_win)

		game_mode_menu = tkinter.Menu(menu_bar, tearoff=0)
		game_mode_menu.add_radiobutton(label="Human vs Human - Local", variable=self.game_mode, value='vs Human - Local', command=lambda: menu_bar.entryconfig('Game Difficulty', state='disabled'))
		game_mode_menu.add_radiobutton(label="Human vs AI", variable=self.game_mode, value='vs AI', command=lambda: menu_bar.entryconfig('Game Difficulty', state='active'))
		menu_bar.add_cascade(label='Game Mode', menu=game_mode_menu)

		game_diff_menu = tkinter.Menu(menu_bar, tearoff=0)
		game_diff_menu.add_radiobutton(label="Easy", variable=self.game_diff, value="easy")
		game_diff_menu.add_radiobutton(label="Normal", variable=self.game_diff, value="normal")
		game_diff_menu.add_radiobutton(label="Hard", variable=self.game_diff, value="hard")
		game_diff_menu.add_radiobutton(label="Overlord", variable=self.game_diff, value="overlord")
		menu_bar.add_cascade(label='Game Difficulty', menu=game_diff_menu)
		menu_bar.entryconfig('Game Difficulty', state='disabled')
		
		self.main_win.config(menu=menu_bar)

		# Column Buttons
		btn_canvas = tkinter.Canvas(self.main_win)
		btn_canvas.grid(row=0, column=0)
		for i in range(7):
			btn = tkinter.Button(btn_canvas, height=2, width=13, command=lambda i=i: self.play_move(i), text='Red')
			btn.grid(row=0, column=i)
			self.col_btns.append(btn)
		self.change_col_btns_states('disabled')
		
		# Canvas & Board
		self.board_canvas.grid(row=1, column=0, columnspan=7)
		for j in range(6):
			for i in range(7):
				slot = self.board_canvas.create_oval((i*100)+5,(j*100)+5,(i*100)+95,(j*100)+95, fill='white')
				self.board_slots.append(slot)
		# initializing after circles so that it is placed on top of the circles
		self.winner_text = self.board_canvas.create_text(350, 300, text='', fill='black', font=('Helvetica 24 bold'))
		
		# Start Button
		start_btn = tkinter.Button(self.main_win, height=2, width=100, command=self.start, text='Start')
		start_btn.grid(row=2, column=0, columnspan=7)

		# Status Bar
		self.status_bar.grid(row=3, column=0, columnspan=7)
	
	def change_col_btns_states(self, new_state):
		for btn in self.col_btns:
			btn.configure(state=new_state)
	
	def fill_gui_board(self):
		for i in range(42):
			if self.c4board.board[i] == -1:
				self.board_canvas.itemconfigure(self.board_slots[i], fill='red', outline='black')
			elif self.c4board.board[i] == 1:
				self.board_canvas.itemconfigure(self.board_slots[i], fill='yellow', outline='black')
			else:
				self.board_canvas.itemconfigure(self.board_slots[i], fill='white', outline='black', width=1)
		# highlight last dropped slot/disk
		if self.c4board.lastPlayedPosition is not None:
			self.board_canvas.itemconfigure(self.board_slots[self.c4board.lastPlayedPosition], outline='orange', width=2.5)
		self.main_win.update()
	
	def start(self):
		if self.game_mode.get() == 'vs AI':
			if self.game_diff.get() == 'easy': agentMaxIter, agentTimeout = 500, 2.5
			elif self.game_diff.get() == 'normal': agentMaxIter, agentTimeout = 2500, 5
			elif self.game_diff.get() == 'hard': agentMaxIter, agentTimeout = 7000, 7
			elif self.game_diff.get() == 'overlord': agentMaxIter, agentTimeout = 25000, 25

			self.mcts_agent = C4_MCTSAgent(self.c4board, 'X', 1, maxIter=agentMaxIter, timeout=agentTimeout, verbose=False, ui='GUI')
		
		# if moveCount is > 0, and Start button is pressed, then we reset.
		if self.c4board.moveCount: self.reset()
		self.status_text.set(f'Human {self.game_mode.get()}')
		
		self.change_col_btns_states('active')
		self.status_bar.update()
	
	def reset(self):
		self.c4board.resetBoard()
		self.fill_gui_board()
		self.change_col_btns_states('active')
		self.board_canvas.itemconfig(self.winner_text, text='')
		for btn in self.col_btns:
			btn.configure(text='Red')
		# reset playerCharToggler and playerNumToggler
		self.playerCharToggler = cycle(['O', 'X'])
		self.playerNumToggler = cycle([-1, 1])
	
	def play_move(self, position):
		cPNum = next(self.playerNumToggler)
		
		if self.game_mode.get() == 'vs AI':
			if cPNum == -1:
				for btn in self.col_btns:
					btn.configure(text='Red')
			elif cPNum == 1:
				for btn in self.col_btns:
					btn.configure(text='Yellow')
		elif self.game_mode.get() == 'vs Human - Local':
			if cPNum == -1:
				for btn in self.col_btns:
					btn.configure(text='Yellow')
			elif cPNum == 1:
				for btn in self.col_btns:
					btn.configure(text='Red')
		
		if not self.c4board.makeMove(cPNum, position):
			self.status_text.set('Position already occupied or Invalid...')
			cPNum = next(self.playerNumToggler)
			return
		
		if self.game_mode.get() == 'vs Human - Local':
			self.fill_gui_board()
			if self.check_game_status(): return
		elif self.game_mode.get() == 'vs AI':
			self.change_col_btns_states('disabled')
			self.status_text.set('AI is thinking...')
			self.fill_gui_board()
			if self.check_game_status(): return
			self.mcts_agent.setNodeMove(-self.mcts_agent.pNum, position)
			agent_position = self.mcts_agent.getMove()
			self.c4board.makeMove(self.mcts_agent.pNum, agent_position)
			self.mcts_agent.setNodeMove(self.mcts_agent.pNum, agent_position)
			next(self.playerNumToggler)
			self.fill_gui_board()
			self.status_text.set(f'AI win probability: {self.mcts_agent.lastWinProbability:.2f}%. Your turn...')
			self.change_col_btns_states('active')
			if self.check_game_status(): return
	
	def check_game_status(self):
		if self.c4board.moveCount > 6:
			status = self.c4board.checkWin()
			if status == 0:
				self.status_text.set('Game Draw!')
				self.board_canvas.itemconfig(self.winner_text, text='Game Draw!')
				self.change_col_btns_states('disabled')
			elif status == -1:
				self.status_text.set('Player Red Wins!')
				self.board_canvas.itemconfig(self.winner_text, text='Player Red Wins!')
				self.change_col_btns_states('disabled')
			elif status == 1:
				self.status_text.set('Player Yellow Wins!')
				self.board_canvas.itemconfig(self.winner_text, text='Player Yellow Wins!')
				self.change_col_btns_states('disabled')
			self.main_win.update()
			return True if status in [0, -1, 1] else False
		return False
		

if __name__ == '__main__':
	gui = C4GUIClient()
	gui.main_win.mainloop()