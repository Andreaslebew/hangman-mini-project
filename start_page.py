import tkinter as tk

class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E8D26B")

        tk.Label(self, text="hangman",
                 font=("Arial", 28, "bold"),
                 bg="#E8D26B").pack(pady=20)

        tk.Label(self, text="PILIH KATEGORI KATA:",
                 font=("Arial", 14),
                 bg="#E8D26B").pack()

        self.category = tk.StringVar(value="Animals")

        for cat in ["Animals", "Fruits", "Cities"]:
            tk.Radiobutton(self, text=cat.lower(),
                           variable=self.category,
                           value=cat,
                           bg="#E8D26B").pack()

        tk.Button(self, text="start",
                  font=("Arial", 16, "bold"),
                  command=self.start).pack(pady=20)

    def start(self):
        self.master.start_game(self.category.get())