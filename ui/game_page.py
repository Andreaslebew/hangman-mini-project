import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

class GamePage(tk.Frame):
    def __init__(self, master, category):
        super().__init__(master, bg="#E8D26B")

        self.category = category
        self.max_hp = 6
        self.hp = self.max_hp
        self.score = 0
        self.guessed_letters = set()
        self.timer_id = None

        self.load_images()
        self.build_ui()
        self.load_word()

    # ================= LOAD PNG =================
    def load_images(self):
        self.images = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)

        for i in range(self.max_hp + 1):
            filename = f"hangman_{i+1}.png"
            path = os.path.join(base_dir, "assets", "hangman", filename)

            if os.path.exists(path):
                img = Image.open(path).resize((200, 200))
                self.images.append(ImageTk.PhotoImage(img))
            else:
                print(f"GAGAL: Gambar tidak ditemukan di path: {path}")
                self.images.append(None)

    # ================= UI =================
    def build_ui(self):
        # TOP BAR
        top = tk.Frame(self, bg="#E8D26B")
        top.pack(fill="x", pady=5)

        tk.Button(top, text="Back",
                  command=self.master.show_start).pack(side="left", padx=10)

        self.timer_label = tk.Label(top, text="Waktu: 30s", 
                                    bg="#E8D26B", fg="red", font=("Arial", 12, "bold"))
        self.timer_label.pack(side="left", expand=True)

        tk.Label(top, text=f"Category: {self.category}",
                 bg="#E8D26B").pack(side="right", padx=10)

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
        bottom.pack(fill="x", pady=10)

        self.hp_label = tk.Label(bottom, text="HP: 6", bg="#E8D26B", font=("Arial", 12))
        self.hp_label.pack(side="left", padx=10)

        self.score_label = tk.Label(bottom, text="Score: 0", bg="#E8D26B", font=("Arial", 12))
        self.score_label.pack(side="left")

    # ================= WORD (PLACEHOLDER) =================
    def load_word(self):
        words = {
            "Animals": ["ELEPHANT", "FROG", "BIRD", "GIRAFFE", "MONKEY", "CHICKEN", "TIGER", "LION"],
            "Fruits": ["PINEAPPLE", "APPLE", "BANANA", "MANGO", "ORANGE"],
            "Cities": ["PASURUAN", "MALANG", "SIDOARJO", "SURABAYA", "JEMBER", "BANYUWANGI"]
        }

        self.word = random.choice(words[self.category])
        self.hp = self.max_hp
        self.guessed_letters = {self.word[0], self.word[1]}

        self.update_word()
        self.update_hp()
        self.update_image()

        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            
        self.time_left = 30
        self.timer_label.config(text=f"Waktu: {self.time_left}s")
        self.countdown()

    def update_word(self):
        text = " ".join([c if c in self.guessed_letters else "_" for c in self.word])
        self.word_var.set(text)

    # ================= TIMER =================
    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Waktu: {self.time_left}s")
            # Loop setiap 1000 milidetik (1 detik)
            self.timer_id = self.after(1000, self.countdown)
        else:
            self.game_over("Waktu Habis!")

    # ================= IMAGE UPDATE =================
    def update_image(self):
        index = self.max_hp - self.hp
        img = self.images[index]

        if img:
            self.image_label.config(image=img)
            self.image_label.image = img

    # ================= GAME LOGIC =================
    def check_win(self):
        # Jika sudah tidak ada garis bawah "_", berarti tebakan benar semua
        if "_" not in self.word_var.get():
            # Matikan timer
            if self.timer_id is not None:
                self.after_cancel(self.timer_id)
                self.timer_id = None
                
            # Hitung skor: (sisa_hp / max_hp) * 100
            score_didapat = int((self.hp / self.max_hp) * 100)
            self.score += score_didapat
            self.score_label.config(text=f"Score: {self.score}")
            
            messagebox.showinfo("Menang!", f"Selamat!\nKata: {self.word}\nSisa nyawa: {self.hp}\nSkor didapat: +{score_didapat}")
            self.load_word()

    def game_over(self, alasan="Game Over"):
        # Matikan timer
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        messagebox.showinfo(alasan, f"Anda Kalah!\nKata yang benar adalah: {self.word}")
        self.load_word()

    # ================= EVENTS =================
    def confirm(self):
        letter = self.entry.get().upper().strip()
        self.entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            return

        if letter in self.word:
            self.guessed_letters.add(letter)
            self.update_word()
            self.check_win()
        else:
            self.hp -= 1
            self.update_hp()
            self.update_image()

            if self.hp <= 0:
                self.game_over("Nyawa Habis!")

    def hint(self):
        hidden = [c for c in self.word if c not in self.guessed_letters]

        if len(hidden) >= 2:
            self.guessed_letters.add(hidden[0])
            self.guessed_letters.add(hidden[1])
            self.hp -= 1

            self.update_word()
            self.update_hp()
            self.update_image()

            if self.hp <= 0:
                self.game_over("Nyawa Habis!")
            else:
                self.check_win()

    def update_hp(self):
        self.hp_label.config(text=f"HP: {self.hp}")
