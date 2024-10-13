import tkinter as tk
from tkinter import messagebox
import random

class MatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelime Eşleştirme Oyunu")
        self.root.attributes("-fullscreen", True)  # Tam ekran modu

        # Sabit boyutlu bir oyun alanı (800x600), tam ekran modunda ortalanır
        self.canvas_frame = tk.Frame(self.root, width=800, height=600, bg="lightblue")
        self.canvas_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Ortalamak için

        # Kelime ve paragraf listeleri (10 kelime ve 10 boşluklu paragraf)
        self.words = ["Elma", "Bilgisayar", "Python", "Araba", "Masa", "Kitap", "Telefon", "Televizyon", "Yazılım", "Kalem"]
        self.paragraphs = [
            "______ bir meyvedir.",
            "______ bir programlama dilidir.",
            "______ bir taşıttır.",
            "______ bir elektronik cihazdır.",
            "______ bir mobilyadır.",
            "______ okunur.",
            "______ bir iletişim aracıdır.",
            "______ bir eğlence aracıdır.",
            "______ bilgisayarlarda kullanılır.",
            "______ bir yazı aracıdır."
        ]

        self.correct_matches = {
            "Elma": 0,
            "Bilgisayar": 1,
            "Araba": 2,
            "Python": 3,
            "Masa": 4,
            "Kitap": 5,
            "Telefon": 6,
            "Televizyon": 7,
            "Yazılım": 8,
            "Kalem": 9
        }

        # Sürüklenen kelime için başlangıç pozisyonu
        self.drag_data = {"word": None, "start_x": 0, "start_y": 0, "offset_x": 0, "offset_y": 0}

        # Rastgele sıralı kelimeler
        self.shuffled_words = random.sample(self.words, len(self.words))

        # En uzun kelimenin genişliğini bulalım
        longest_word = max(self.words, key=len)

        # Ekrana sabit genişlikteki paragraf ve kelime kutularını yerleştirme
        self.frame = tk.Frame(self.canvas_frame)
        self.frame.pack(expand=True)

        # Kelimelerin genişliğini en büyük kelimeye göre set edelim
        max_word_width = len(longest_word) + 5  # Fazladan boşluk ekledik

        # En uzun kelimenin genişliğine göre paragraflardaki "______" boşluğunu ayarla
        max_blank_width = max_word_width

        # Paragrafları ve kelimeleri yan yana ekleyelim
        self.drop_labels = []
        self.word_labels = []
        for i, paragraph in enumerate(self.paragraphs):
            # "______" boşluğunu en uzun kelimenin genişliğine göre ayarla
            adjusted_paragraph = paragraph.replace("______", " " * max_blank_width)

            # Yuvarlak köşeli ve mavi tonlu arka plana sahip paragraf kutusu
            paragraph_label = tk.Label(self.frame, text=adjusted_paragraph, bg="lightblue", padx=10, pady=5, relief="solid", bd=2, width=max_blank_width + 30, wraplength=330)
            paragraph_label.grid(row=i, column=0, padx=10, pady=10)

            # Yuvarlak köşeli boşluk kutusu (drop area)
            drop_label = tk.Label(self.frame, text="______", bg="lightblue", width=max_blank_width, padx=10, pady=5, relief="solid", bd=2, wraplength=100)
            drop_label.grid(row=i, column=1, padx=50, pady=10)  # `padx` değeri artırıldı
            self.drop_labels.append(drop_label)

            # Kelimeleri paragrafların sağ tarafına ekleyelim
            label = tk.Label(self.frame, text=self.shuffled_words[i], bg="lightgray", width=max_word_width, padx=10, pady=5, relief="solid", bd=2, wraplength=100)
            label.grid(row=i, column=2, padx=10, pady=10)
            label.bind("<Button-1>", self.start_drag)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", self.stop_drag)
            self.word_labels.append(label)

        # Sabit boyutlu butonlar için genişlik ayarı
        button_width = 20

        # Sonuçları kontrol etme butonu (aynı boyutta)
        check_button = tk.Button(self.frame, text="Sonuçları Kontrol Et", command=self.check_answers, width=button_width, padx=10, pady=5)
        check_button.grid(row=len(self.paragraphs) + 1, column=0, pady=10)

        # Reset butonu (aynı boyutta)
        reset_button = tk.Button(self.frame, text="Reset", command=self.reset_game, width=button_width, padx=10, pady=5)
        reset_button.grid(row=len(self.paragraphs) + 1, column=1, pady=10)

        # Exit butonu (aynı boyutta)
        exit_button = tk.Button(self.frame, text="Exit", command=self.exit_game, width=button_width, padx=10, pady=5)
        exit_button.grid(row=len(self.paragraphs) + 1, column=2, pady=10)

        self.matches = {}

    def start_drag(self, event):
        """Sürükleme işlemi başladığında çağrılır"""
        label = event.widget
        self.drag_data["word"] = label
        self.drag_data["offset_x"] = event.x_root - label.winfo_x()  # Fare ile kelimenin sol üst köşesi arasındaki fark
        self.drag_data["offset_y"] = event.y_root - label.winfo_y()
        label.lift()  # Kelimenin her zaman en önde olmasını sağlamak için

    def on_drag(self, event):
        """Sürükleme işlemi sırasında çağrılır"""
        label = self.drag_data["word"]
        # Kelimeyi fare imlecinin ucunda tutmak için hesaplanan farkı kullan
        x = event.x_root - self.drag_data["offset_x"]
        y = event.y_root - self.drag_data["offset_y"]
        label.place(x=x, y=y)

    def stop_drag(self, event):
        """Sürükleme işlemi bittiğinde çağrılır"""
        label = self.drag_data["word"]
        placed = False

        # Eğer kelime boşluğun üstünde bırakılmışsa yerleşsin
        for drop_label in self.drop_labels:
            if self.is_overlapping(label, drop_label):
                drop_label.config(text=label["text"], bg="lightblue")
                placed = True
                label.place_forget()  # Kelimeyi ortadan kaldır
                break

        if not placed:
            # Eğer kelime boşluğa bırakılmadıysa, eski yerine geri dönsün
            label.grid(row=self.word_labels.index(label), column=2, padx=10, pady=10)

        self.drag_data["word"] = None

    def is_overlapping(self, widget1, widget2):
        """İki widget'ın üst üste gelip gelmediğini kontrol eder"""
        x1, y1, x2, y2 = widget1.winfo_rootx(), widget1.winfo_rooty(), widget1.winfo_rootx() + widget1.winfo_width(), widget1.winfo_rooty() + widget1.winfo_height()
        x1_d, y1_d, x2_d, y2_d = widget2.winfo_rootx(), widget2.winfo_rooty(), widget2.winfo_rootx() + widget2.winfo_width(), widget2.winfo_rooty() + widget2.winfo_height()

        return x1 < x2_d and x2 > x1_d and y1 < y2_d and y2 > y1_d

    def check_answers(self):
        correct_count = 0
        for i, drop_label in enumerate(self.drop_labels):
            word = drop_label.cget("text")
            if word in self.correct_matches and self.correct_matches[word] == i:
                correct_count += 1

        messagebox.showinfo("Sonuç", f"Doğru eşleştirmeler: {correct_count}/{len(self.words)}")

    def reset_game(self):
        """Oyunu sıfırlar"""
        # Tüm drop alanlarını temizle
        for drop_label in self.drop_labels:
            drop_label.config(text="______", bg="lightblue")

        # Kelimeleri başlangıç pozisyonuna geri döndür
        for i, label in enumerate(self.word_labels):
            label.grid(row=i, column=2, padx=10, pady=10)

    def exit_game(self):
        """Oyundan çıkış yapar"""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchGame(root)
    root.mainloop()