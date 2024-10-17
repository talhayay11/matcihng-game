import tkinter as tk
from tkinter import messagebox
import random

class MatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelime Eşleştirme Oyunu")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="white")

        self.title_label = tk.Label(self.root, text="Complete the sentences with the given words in “Simple Past”.", bg="white", fg="black", font=("Arial", 24, "bold"))
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.canvas_frame = tk.Frame(self.root, width=800, height=600, bg="lightblue")
        self.canvas_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.words = ["start", "give", "fly", "notice", "get up"]

        self.word_options = {
            "start": ["start", "started"],
            "give": ["give", "gave"],
            "fly": ["fly", "flew"],
            "notice": ["notice", "noticed"],
            "get up": ["get up", "got up"]
        }

        self.paragraphs = [
            "They ____ to Paris by Turkish Airlines.",
            "Patrick ____ playing soccer at the age of seven.",
            "Rosa ____ very early this morning because she had an exam.",
            "Our trainer ____ Cansu’s talent and advised her to play for a volleyball club",
            "Mrs. Jones ____ her students a lecture on legendary figures and great people in history.",
        ]

        self.correct_matches = {
            "flew": 0,
            "started": 1,
            "got up": 2,
            "noticed": 3,
            "gave": 4,
        }

        self.drag_data = {"word": None, "start_x": 0, "start_y": 0, "offset_x": 0, "offset_y": 0}

        self.shuffled_words = random.sample(self.words, len(self.words))

        self.drop_labels = []
        self.word_labels = []
        for i, paragraph in enumerate(self.paragraphs):
            paragraph_part1 = paragraph.split("____")[0]
            paragraph_part2 = paragraph.split("____")[1]

            label1 = tk.Label(self.canvas_frame, text=paragraph_part1, bg="white", padx=20, pady=12, font=("Arial", 16))
            label1.grid(row=i, column=0, sticky="e", padx=(20, 5))

            drop_label = tk.Label(self.canvas_frame, text="____", bg="lightblue", width=12, padx=20, pady=12, relief="solid", bd=2, font=("Arial", 16))
            drop_label.grid(row=i, column=1, padx=1, pady=10)
            self.drop_labels.append(drop_label)

            label2 = tk.Label(self.canvas_frame, text=paragraph_part2, bg="white", padx=25, pady=12, font=("Arial", 16))
            label2.grid(row=i, column=2, sticky="w", padx=(5, 50))

            label = tk.Label(self.canvas_frame, text=self.shuffled_words[i], bg="lightgray", padx=25, pady=12, relief="solid", bd=2, font=("Arial", 16))
            label.grid(row=i, column=3, padx=10, pady=10)
            label.bind("<Button-1>", self.start_drag)
            label.bind("<Button-3>", self.show_options)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", self.stop_drag)
            self.word_labels.append(label)

        button_width = 20

        check_button = tk.Button(self.canvas_frame, text="Check The Answers", command=self.check_answers, width=button_width, padx=10, pady=5)
        check_button.grid(row=len(self.paragraphs), column=0, pady=(20, 10))

        reset_button = tk.Button(self.canvas_frame, text="Reset", command=self.reset_game, width=button_width, padx=10, pady=5)
        reset_button.grid(row=len(self.paragraphs), column=1, pady=(20, 10))

        exit_button = tk.Button(self.canvas_frame, text="Exit", command=self.exit_game, width=button_width, padx=10, pady=5)
        exit_button.grid(row=len(self.paragraphs), column=2, pady=(20, 10))

        self.matches = {}

    def show_options(self, event):
        label = event.widget
        word = label.cget("text")
        options = self.word_options[word]

        option_window = tk.Toplevel(self.root)
        option_window.title(f"Choose form for '{word}'")

        x, y = event.x_root, event.y_root
        option_window.geometry(f"+{x - 200}+{y + 20}")

        option_window.geometry("300x200")

        tk.Label(option_window, text=f"Choose a form for '{word}':", font=("Arial", 16)).pack(pady=15)

        for option in options:
         option_button = tk.Button(option_window, text=option, font=("Arial", 16), command=lambda opt=option: self.set_word_form(label, opt, option_window))
         option_button.pack(pady=10)

    def set_word_form(self, label, option, window):
        label.config(text=option)
        window.destroy()


    def start_drag(self, event):
      label = event.widget
      self.drag_data["word"] = label
      self.drag_data["offset_x"] = event.x_root - label.winfo_x()
      self.drag_data["offset_y"] = event.y_root - label.winfo_y()

      self.drag_data["original_row"] = label.grid_info()["row"]
      self.drag_data["original_col"] = label.grid_info()["column"]

      label.lift()

    def on_drag(self, event):
        label = self.drag_data["word"]
        x = event.x_root - self.drag_data["offset_x"]
        y = event.y_root - self.drag_data["offset_y"]
        label.place(x=x, y=y)

    def stop_drag(self, event):
      label = self.drag_data["word"]
      placed = False

      for drop_label in self.drop_labels:
        if self.is_overlapping(label, drop_label):
            drop_label.config(text=label["text"], bg="lightblue")
            placed = True
            label.place_forget()
            break

      if not placed:
        label.grid(row=self.drag_data["original_row"], column=self.drag_data["original_col"], padx=10, pady=10)

      self.drag_data["word"] = None

    def is_overlapping(self, widget1, widget2):
        x1, y1, x2, y2 = widget1.winfo_rootx(), widget1.winfo_rooty(), widget1.winfo_rootx() + widget1.winfo_width(), widget1.winfo_rooty() + widget1.winfo_height()
        x1_d, y1_d, x2_d, y2_d = widget2.winfo_rootx(), widget2.winfo_rooty(), widget2.winfo_rootx() + widget2.winfo_width(), widget2.winfo_rooty() + widget2.winfo_height()

        return x1 < x2_d and x2 > x1_d and y1 < y2_d and y2 > y1_d

    def check_answers(self):
        correct_count = 0
        for i, drop_label in enumerate(self.drop_labels):
            word = drop_label.cget("text")
            if word in self.correct_matches and self.correct_matches[word] == i:
                correct_count += 1

        messagebox.showinfo("Result", f"Correct Answers: {correct_count}/{len(self.words)}")

    def reset_game(self):
        for drop_label in self.drop_labels:
            drop_label.config(text="____", bg="lightblue")

        for i, label in enumerate(self.word_labels):
         label.config(text=self.shuffled_words[i])
         label.grid(row=i, column=4, padx=19, pady=10)

    def exit_game(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchGame(root)
    root.mainloop()