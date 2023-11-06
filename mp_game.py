from tkinter import *
from utils import Utils, update_for_winner, save_w_Size, load_config, change_theme, play_sound

class TTT:
    def __init__(self, root,prev):
        self.config = load_config()
        self.button_list = []
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.grid_list = []
        self.current_p = "O"
        self.root = root
        self.prev = prev
        self.max_depth = 0
        self.diff = [1,2]
    def set_current_p(self):
        self.current_p = "X" if self.current_p == "O" else "O"
    def place_mark(self, i, j):
        self.grid_list[i][j].config(text=self.current_p)
        self.grid_list[i][j].config(state="disabled")
        self.grid_list[i][j].grid(row=i, column=j, sticky="nsew")
    def highlight_winning_cells(self, rows, cols):
        highlight = change_theme(self.root, self.config["theme"])
        for row, col in zip(rows,cols):
            self.grid_list[row][col].config(bg=highlight)
    def is_draw(self):
        for i in range(3):
            for j in range(3):
                if self.grid_list[i][j].cget("text") == "":
                    return False
        return True
    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        save_w_Size(self.root)
        self.root.destroy()
        self.prev.deiconify()
        
    def create_board(self):
        for i in range(3):
            temp_list = []
            for j in range(3):
                button = Button(self.root, text="", command=lambda r=i, c=j: [play_sound(),self.place_mark(r,c),update_for_winner(self),self.set_current_p()])
                button.grid(row=i, column=j, sticky="nsew")
                temp_list.append(button)
                self.button_list.append(button)
            self.grid_list.append(temp_list)
        for i in range(3):
            for j in range(3):
                Grid.columnconfigure(self.root, j, weight=1)
                Grid.rowconfigure(self.root, i, weight=1)
        u = Utils(self.root, self.button_list)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        change_theme(self.root, self.config["theme"])
        self.root.bind("<Configure>", u.resize)
        self.root.mainloop()