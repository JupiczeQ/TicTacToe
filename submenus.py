from tkinter import *
from utils import init_utils, save_w_Size, create_Window, load_config, change_theme
from sp_game import MiniMax
from mp_game import TTT
from sound_menu import soundMenu
from theme_menu import themeMenu

class optionsMenu:
    def __init__(self, prev):
        self.config = load_config()
        self.prev = prev
    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        save_w_Size(self.root)
        self.root.destroy()
        self.prev.deiconify()
    def options_menu(self):
        self.prev.withdraw()
        root = create_Window("Opcje")
        self.root = root
        sound = soundMenu(root)
        theme = themeMenu(root)
        sound_button = Button(root, text="Opcje dzwięku", command=lambda: sound.sound_m())
        theme_button = Button(root, text="Zmień motyw", command=lambda: theme.theme_m())
        to_main_button = Button(root, text="Wróć", command=lambda: [self.on_closing()])
        button_list = [sound_button, theme_button, to_main_button]
        change_theme(root, self.config["theme"])
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        init_utils(root, button_list)  
class spClass:
    def __init__(self, prev):
        self.config = load_config()
        self.prev = prev
    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        save_w_Size(self.root)
        self.root.destroy()
        self.prev.deiconify()
    def c_board(self, root, max_depth):
        board = MiniMax(root, max_depth)
        board.create_board()
    def sp_submenu(self):
        self.prev.withdraw()
        root = create_Window("Tryb jednoosobowy")
        self.root = root
        ez_button = Button(root, text="Poziom łatwy", command=lambda: [save_w_Size(root), self.c_board(root, 4)])
        mid_button = Button(root, text="Poziom średni", command=lambda: [save_w_Size(root), self.c_board(root, 7)])
        hard_button = Button(root, text="Poziom trudny", command=lambda: [save_w_Size(root), self.c_board(root, 9)])
        to_main_button = Button(root, text="Wróć", command=lambda: [self.on_closing()])
        button_list = [ez_button, mid_button, hard_button, to_main_button]
        change_theme(root, self.config["theme"])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        init_utils(root, button_list)

def mp_submenu(prev):
    prev.withdraw()
    root = create_Window("Tryb dwuosobowy")
    board = TTT(root,prev)
    board.create_board()
        