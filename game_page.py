import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class GamePage(tk.Frame):
    def __init__(self, master, category):
        super().__init__(master, bg="#E8D26B")

        self.category = category
        self.max_hp = 6
        self.hp = self.max_hp
        self.score = 0
        self.guessed_letters = set()

        self.load_images()
        self.build_ui()
        self.load_word()

    # ================= LOAD PNG =================
    def load_images(self):
        self.images = []
        for i in range(self.max_hp + 1):
            path = f"assets/hangman/hangman_{i}.png"
            if os.path.exists(path):
                img = Image.open(path).resize((200, 200))
                self.images.append(ImageTk.PhotoImage(img))
            else:
                self.images.append(None)

    # ================= UI =================
    def build_ui(self):
        # TOP BAR
        top = tk.Frame(self, bg="#E8D26B")
        top.pack(fill="x")

        tk.Button(top, text="Back",
                  command=self.master.show_start).pack(side="left")

        tk.Label(top, text=f"Category: {self.category}",
                 bg="#E8D26B").pack(side="right")

        # MAIN
        main = tk.Frame(self, bg="#E8D26B")
        main.pack(expand=True, fill="both")

        # LEFT (IMAGE)
        left = tk.Frame(main, bg="#E8D26B")
        left.pack(side="left", expand=True)

        self.image_label = tk.Label(left, bg="#E8D26B")
        self.image_label.pack(pady=20)

        self.word_var = tk.StringVar()
        tk.Label(left, textvariable=self.word_var,
                 font=("Courier", 28),
                 bg="#E8D26B").pack()

        # RIGHT (INPUT)
        right = tk.Frame(main, bg="#E8D26B")
        right.pack(side="right", padx=20)

        tk.Label(right, text="Input Letter",
                 bg="#E8D26B").pack()

        self.entry = tk.Entry(right, font=("Arial", 18), width=5, justify="center")
        self.entry.pack(pady=10)

        tk.Button(right, text="Confirm",
                  command=self.confirm).pack(pady=5)

        tk.Button(right, text="Hint",
                  command=self.hint).pack(pady=5)

        tk.Button(right, text="Next",
                  command=self.load_word).pack(pady=5)

        # BOTTOM
        bottom = tk.Frame(self, bg="#E8D26B")
        bottom.pack(fill="x")

        self.hp_label = tk.Label(bottom, text="HP: 6", bg="#E8D26B")
        self.hp_label.pack(side="left", padx=10)

        self.score_label = tk.Label(bottom, text="Score: 0", bg="#E8D26B")
        self.score_label.pack(side="left")

    # ================= WORD (PLACEHOLDER) =================
    def load_word(self):
        words = {
            "Animals": "ELEPHANT",
            "Fruits": "PINEAPPLE",
            "Cities": "LONDON"
        }

        self.word = words[self.category]
        self.hp = self.max_hp
        self.guessed_letters = {self.word[0], self.word[1]}

        self.update_word()
        self.update_hp()
        self.update_image()

    def update_word(self):
        text = " ".join([c if c in self.guessed_letters else "_" for c in self.word])
        self.word_var.set(text)

    # ================= IMAGE UPDATE =================
    def update_image(self):
        index = self.max_hp - self.hp
        img = self.images[index]

        if img:
            self.image_label.config(image=img)
            self.image_label.image = img

    # ================= EVENTS =================
    def confirm(self):
        letter = self.entry.get().upper().strip()
        self.entry.delete(0, tk.END)

        if not letter.isalpha():
            return

        if letter in self.word:
            self.guessed_letters.add(letter)
            self.update_word()
        else:
            self.hp -= 1
            self.update_hp()
            self.update_image()

            if self.hp <= 0:
                messagebox.showinfo("Game Over", self.word)
                self.load_word()

    def hint(self):
        hidden = [c for c in self.word if c not in self.guessed_letters]

        if len(hidden) >= 2:
            self.guessed_letters.add(hidden[0])
            self.guessed_letters.add(hidden[1])
            self.hp -= 1

            self.update_word()
            self.update_hp()
            self.update_image()

    def update_hp(self):
        self.hp_label.config(text=f"HP: {self.hp}")