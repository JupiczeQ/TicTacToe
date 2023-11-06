from tkinter import *
from tkinter import messagebox
from random import randint
import json
import os
from pygame import mixer

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as json_file:
            return json.load(json_file)
    else:
        with open("config_defaults.json", "r") as json_file:
            return json.load(json_file)

class Utils:
    def __init__(self,root,button_list):
        self.root = root
        self.button_list = button_list
        self.config = load_config()
    def save_w_Size(root):
        conifg = load_config()
        current_width = root.winfo_width()
        current_height = root.winfo_height()
        size = ("{}x{}").format(current_width, current_height)
        conifg["size"] = size
        with open("config.json", "w") as json_file:
            json.dump(conifg, json_file)
    def configure_size(self):
        i=0
        Grid.columnconfigure(self.root, 0, weight=1)
        for button in self.button_list:
            button.grid(row = i, column=0, sticky="nsew")
            Grid.rowconfigure(self.root, i, weight=1)
            i+=1
        change_theme(self.root, self.config["theme"])
    def resize(self, e):
        if e.width != self.root.winfo_width() or e.height != self.root.winfo_height():
            size_w = e.width / 15
            size_h = e.height / 15
            size = (size_h + size_w) / 2
            for button in self.button_list:
                button.config(font=("Helvetica", int(size)))
def init_utils(root, button_list):
    u = Utils(root, button_list)
    u.configure_size()
    root.bind("<Configure>", u.resize)
    root.mainloop()

def save_w_Size(root):
    conifg = load_config()
    current_width = root.winfo_width()
    current_height = root.winfo_height()
    size = ("{}x{}").format(current_width, current_height)
    conifg["size"] = size
    with open("config.json", "w") as json_file:
        json.dump(conifg, json_file)

def create_Window(name):
    size = load_config()["size"]
    root = Tk()
    root.geometry(size)
    root.minsize(225,100)
    root.title(name)
    return root

def disable_all_buttons(grid):
    for row in grid:
        for button in row:
            button.config(state="disabled")

def update_for_winner(self):
    is_winner = False
    for i in range(3):
        if self.grid_list[i][0].cget("text") == self.grid_list[i][1].cget("text") == self.grid_list[i][2].cget("text") != "":
            self.highlight_winning_cells([i, i, i], [0, 1, 2])
            is_winner = True
        if self.grid_list[0][i].cget("text") == self.grid_list[1][i].cget("text") == self.grid_list[2][i].cget("text") != "":
            self.highlight_winning_cells([0, 1, 2], [i, i, i])
            is_winner = True
    if self.grid_list[0][0].cget("text") == self.grid_list[1][1].cget("text") == self.grid_list[2][2].cget("text") != "":
        self.highlight_winning_cells([0, 1, 2], [0, 1, 2])
        is_winner = True
    if self.grid_list[0][2].cget("text") == self.grid_list[1][1].cget("text") == self.grid_list[2][0].cget("text") != "":
        self.highlight_winning_cells([0, 1, 2], [2, 1, 0])
        is_winner = True
    if is_winner or self.is_draw():
        disable_all_buttons(self.grid_list)
        if is_winner:
            messagebox.showinfo("Tic-Tac-Toe", "Wygrywa: " + self.current_p)
        else:
            messagebox.showinfo("Tic-Tac-Toe", "Remis!")
        is_winner = False
        self.grid_list.clear()
        self.button_list.clear()
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        if self.max_depth in self.diff:
            self.x,self.y = randint(0,2), randint(0,2)
            self.board[self.x][self.y] = "X"
        self.create_board()

def play_sound():
    volume = int(load_config()["volume"])
    mixer.music.load("place.mp3")
    mixer.music.set_volume(volume/100)
    mixer.music.play()

def change_theme(root, theme):
    themes = {
    "Light": {"bg": "#fafafa", "clickable": "#dfe0e6", "active": "#e4e5f1", "text": "black"},
    "Dark": {"bg": "#1f1b24", "clickable": "#332940", "active": "#473959" ,"text": "white"}
    }
    theme_colors = themes[theme]
    root.configure(bg=theme_colors["bg"])
    buttons = [widget for widget in root.winfo_children() if isinstance(widget, Button)]
    for button in buttons:
        button.configure(bg=theme_colors["clickable"], fg=theme_colors["text"], activebackground=theme_colors["active"], activeforeground=theme_colors["text"])
    option_menus = [widget for widget in root.winfo_children() if isinstance(widget, OptionMenu)]
    for option_menu in option_menus:
        option_menu.configure(bg=theme_colors["clickable"], fg=theme_colors["text"], highlightbackground=theme_colors["bg"], activebackground=theme_colors["active"], activeforeground=theme_colors["text"])
        menu = option_menu.nametowidget(option_menu.menuname)
        menu.configure(bg=theme_colors["clickable"], fg=theme_colors["text"], activebackground=theme_colors["active"], activeforeground=theme_colors["text"])
    sliders = [widget for widget in root.winfo_children() if isinstance(widget, Scale)]
    for slider in sliders:
        slider.configure(bg=theme_colors["bg"], fg=theme_colors["text"], highlightbackground=theme_colors["bg"], activebackground=theme_colors["active"])
    return theme_colors["active"]
