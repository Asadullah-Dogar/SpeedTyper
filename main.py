import tkinter as tk
from tkinter.ttk import Button
import ctypes
import random

# Enable High DPI awareness (Windows)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Create main application window
app = tk.Tk()
app.title("Typing Speed Test")
app.geometry("700x700")
app.option_add("*Label.Font", "Consolas 20")
app.option_add("*Button.Font", "Consolas 20")


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.possible_texts = [
            "In the heart of the forest, a lone traveler wandered. The trees whispered secrets of the past, their leaves dancing to the rhythm of the wind. The beauty of nature surrounded him, a stark reminder of the simplicity he often overlooked."
            "Artificial intelligence has been a game-changer in modern society. From automating mundane tasks to advancing healthcare and scientific research, its impact is undeniable. However, with great power comes great responsibility, and it’s crucial to address ethical concerns."
            "The concept of time is fascinating. Every second that passes becomes history, and every second ahead is a mystery. Time waits for no one, and yet, it heals all wounds. It’s a paradox that defines our existence."
            "Space exploration has always captured the imagination of humanity. The idea of venturing beyond our planet to discover the mysteries of the universe is as thrilling as it is challenging. With advancements in technology, dreams of interstellar travel may soon become a reality."
            "The small town was abuzz with excitement as the annual festival approached. Brightly colored banners adorned the streets, and the aroma of freshly baked goods filled the air. It was a time for joy, connection, and celebration."
        ]
        self.writeable = True
        self.passed_seconds = 0
        self.reset_writing_labels()

    def reset_writing_labels(self):
        self.text = random.choice(self.possible_texts).lower()
        self.split_point = 0

        # Labels
        self.label_left = tk.Label(self.root, text="", fg="grey")
        self.label_left.place(relx=0.5, rely=0.5, anchor=tk.E)

        self.label_right = tk.Label(self.root, text=self.text, fg="black")
        self.label_right.place(relx=0.5, rely=0.5, anchor=tk.W)

        self.current_letter_label = tk.Label(self.root, text=self.text[0], fg="red")
        self.current_letter_label.place(relx=0.5, rely=0.6, anchor=tk.N)

        self.time_label = tk.Label(self.root, text="0 Seconds", fg="blue")
        self.time_label.place(relx=0.5, rely=0.4, anchor=tk.S)

        # Reset state
        self.writeable = True
        self.passed_seconds = 0

        # Key bindings and timers
        self.root.bind("<Key>", self.key_press)
        self.root.after(60000, self.stop_test)  # Stop test after 60 seconds
        self.root.after(1000, self.add_seconds)  # Update time every second

    def stop_test(self):
        self.writeable = False
        amount_words = len(self.label_left.cget("text").split())

        # Cleanup
        self.time_label.destroy()
        self.current_letter_label.destroy()
        self.label_left.destroy()
        self.label_right.destroy()

        # Display results
        self.result_label = tk.Label(
            self.root, text=f"Words Per Minute: {amount_words}", fg="green"
        )
        self.result_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.result_button = Button(self.root, text="Retry", command=self.restart)
        self.result_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def restart(self):
        self.result_label.destroy()
        self.result_button.destroy()
        self.reset_writing_labels()

    def add_seconds(self):
        if self.writeable:
            self.passed_seconds += 1
            self.time_label.configure(text=f"{self.passed_seconds} Seconds")
            self.root.after(1000, self.add_seconds)

    def key_press(self, event):
        if not self.writeable:
            return

        if event.char.lower() == self.label_right.cget("text")[0].lower():
            self.label_left.configure(
                text=self.label_left.cget("text") + event.char.lower()
            )
            self.label_right.configure(text=self.label_right.cget("text")[1:])

            if self.label_right.cget("text"):
                self.current_letter_label.configure(text=self.label_right.cget("text")[0])
            else:
                self.current_letter_label.configure(text="")


# Initialize and run the app
test_app = TypingSpeedTest(app)
app.mainloop()
