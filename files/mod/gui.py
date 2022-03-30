from cProfile import label
import tkinter as tk

class simple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI")
        self.root.geometry("250x280")

        self.label = tk.Label(self.root, text="Hello World", font=("Arial", 15))
        self.label.place(x=0, y=0, width=250, height=280)
    
    def update(self, text):
        self.label.config(text=text)
        self.label.update()

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()