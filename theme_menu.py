from tkinter import Tk, Button, OptionMenu, StringVar
import json
from utils import load_config, change_theme

class themeMenu:
    def __init__(self, prev):
        self.prev = prev

    def save_theme(self, choice):
        theme = choice.get()
        self.config["theme"] = theme
        change_theme(self.root, theme)
        with open("config.json", "w") as json_file:
            json.dump(self.config, json_file)
    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        self.root.destroy()
        self.prev.deiconify()
    def theme_m(self):
        self.config = load_config()
        theme = self.config["theme"]
        self.prev.withdraw()
        root = Tk()
        root.title("Theme menu")
        root.geometry("225x100")
        root.resizable(False, False)
        self.root = root
        choice = StringVar(root)
        choices = ["Light", "Dark"]
        choice.set(theme)
        drop = OptionMenu(root, choice, *choices)
        drop.pack(expand=True)
        button = Button(root, text="Zapisz", command=lambda: self.save_theme(choice))
        button.pack(expand=True)
        change_theme(root,choice.get())
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.mainloop()