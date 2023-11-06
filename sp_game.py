from tkinter import *
from utils import Utils, create_Window, update_for_winner, save_w_Size, load_config, change_theme, play_sound
from math import inf
from random import randint, choice

class MiniMax:
    def __init__(self,prev, max_depth):
        self.config = load_config()
        self.diff = [7,9]
        self.button_list = []
        self.grid_list = [] 
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.current_p = "O"
        self.x,self.y = randint(0,2), randint(0,2)
        self.prev = prev
        self.max_depth = max_depth
        if max_depth in self.diff:
            self.board[self.x][self.y] = "X"
        self.root = None
    def set_current_p(self):
        self.current_p = "X" if self.current_p == "O" else "O"
    def place_mark(self, i, j, mark):
        self.board[i][j] = mark
        self.grid_list[i][j].config(state="disabled")
    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.grid_list[i][j].config(text=self.board[i][j])
    def check_for_winner(self, board):
        # Check rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
        # Check columns
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] != "":
                return board[0][j]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        # No winner
        return None
    
    def is_draw(self):
        for i in range(3):
            for j in range(3):
                if self.grid_list[i][j].cget("text") == "":
                    return False
        return True

    def highlight_winning_cells(self, rows, cols):
        highlight = change_theme(self.root, self.config["theme"])
        for row, col in zip(rows,cols):
            self.grid_list[row][col].config(bg=highlight)

    def minimax(self,board,depth,isMax):
        scores = {"X": 1, "O": -1}
        result = self.check_for_winner(board)
        if result != None:
            score = scores[result] if result != None else 0
            return score/depth
        if isMax:
            bestScore = -inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        bestScore = min(score, bestScore)
            return bestScore
    
    def best_move(self):
        bestScore = -inf
        bestMove = (0,0)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    tboard = self.board
                    score = self.minimax(tboard, 1, False)
                    self.board[i][j] = ""
                    tboard = self.board
                    if(score > bestScore):
                        bestScore = score
                        bestMove = (i,j)
        self.place_mark(bestMove[0],bestMove[1], "X")
        self.update_board()
        update_for_winner(self)
        self.set_current_p()

    def with_diff(self):
        if randint(1,9) <= self.max_depth:
            self.best_move()
        else:
            empty_slots = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        empty_slots.append((i, j))
            if empty_slots:
                i, j = choice(empty_slots)
                self.place_mark(i, j, "X")
                self.update_board()
                update_for_winner(self)
                self.set_current_p()

    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        save_w_Size(self.root)
        self.root.destroy()
        self.prev.deiconify()

    def create_board(self):
        self.prev.withdraw()
        if self.root == None:
            if self.max_depth == self.diff[0]:
                self.root = create_Window("Poziom średni")
            elif self.max_depth == self.diff[1]:
                self.root = create_Window("Poziom trudny")
            else:
                self.root = create_Window("Poziom łatwy")
        self.current_p = "O"
        for i in range(3):
            temp_list = []
            for j in range(3):
                button = Button(self.root, text="", command=lambda r=i, c=j: [play_sound(), self.place_mark(r,c, "O"), self.update_board(),update_for_winner(self), self.set_current_p(), self.with_diff()])
                button.grid(row=i, column=j, sticky="nsew")
                temp_list.append(button)
                self.button_list.append(button)
            self.grid_list.append(temp_list)
        for i in range(3):
            for j in range(3):
                Grid.columnconfigure(self.root, j, weight=1)
                Grid.rowconfigure(self.root, i, weight=1)
        if self.max_depth in self.diff:
            self.grid_list[self.x][self.y].config(text="X",state="disabled")
        change_theme(self.root, self.config["theme"])
        u = Utils(self.root, self.button_list)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", u.resize)
        self.root.mainloop()