import tkinter as tk
from ui.start_page import StartPage
from ui.game_page import GamePage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman")
        self.geometry("800x500")
        self.resizable(False, False)

        self.current_frame = None
        self.show_start()

    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_start(self):
        self.switch_frame(StartPage)

    def start_game(self, category):
        self.switch_frame(GamePage, category)


if __name__ == "__main__":
    app = App()
    app.mainloop()