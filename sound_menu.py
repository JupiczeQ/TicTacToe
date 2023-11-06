from tkinter import Tk, Scale, Button
import json
from utils import load_config, change_theme

class soundMenu:
    def __init__(self, prev):
        self.prev = prev
    def save_slider_value(self, slider):
        value = slider.get()
        self.config["volume"] = value
        with open("config.json", "w") as json_file:
            json.dump(self.config, json_file)
    def on_closing(self):
        self.config = load_config()
        change_theme(self.prev, self.config["theme"])
        self.root.destroy()
        self.prev.deiconify()
    def sound_m(self):
        self.config = load_config()
        volume = self.config["volume"]
        self.prev.withdraw()
        root = Tk()
        root.title("Menu dzwięku")
        root.geometry("225x100")
        root.resizable(False, False)
        self.root = root
        volume_slider = Scale(root, from_=0, to=100, orient="horizontal", length=205)
        volume_slider.set(volume)
        volume_slider.pack(expand=True)
        button = Button(root, text="Zapisz", command=lambda: self.save_slider_value(volume_slider))
        button.pack(expand=True)
        change_theme(root, self.config["theme"])
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.mainloop()