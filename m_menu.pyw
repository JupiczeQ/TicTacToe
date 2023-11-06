from tkinter import Button
from utils import init_utils, save_w_Size, create_Window, change_theme, load_config
from submenus import spClass, optionsMenu, mp_submenu
from pygame import mixer

def main_menu():
    mixer.init()
    config = load_config()
    root = create_Window("Menu główne")
    sp_sub = spClass(root)
    op_sub = optionsMenu(root)
    sp_button = Button(root, text="Tryb jednoosobowy", command=lambda: [save_w_Size(root),sp_sub.sp_submenu()])
    mp_button = Button(root, text="Tryb dwuosobowy", command=lambda: [save_w_Size(root),mp_submenu(root)])
    options_button = Button(root, text="Opcje", command=lambda: [save_w_Size(root),op_sub.options_menu()])
    exit_button = Button(root, text="Wyjdź", command=lambda: [root.destroy(),root.quit()])
    button_list = [sp_button, mp_button, options_button, exit_button]
    change_theme(root, config["theme"])
    init_utils(root, button_list)
    
main_menu()
x = input()