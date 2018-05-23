import tkinter as tk
from PIL import Image
from PIL import ImageTk


class MeanModelFrame(tk.Frame):

    def __init__(self, parent, img, row, col):
        tk.Frame.__init__(self, parent)

        self.grid(row=row, column=col, sticky="nsew")

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)

        label = tk.Label(self, image=imgtk)
        label.image = imgtk
        label.pack()
