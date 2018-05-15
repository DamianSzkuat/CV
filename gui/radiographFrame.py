import tkinter as tk
from PIL import Image
from PIL import ImageTk


class RadiographFrame(tk.Frame):

    def __init__(self, parent, img):
        tk.Frame.__init__(self, parent)

        self.grid(row=0, column=0, sticky="nsew")

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)

        label = tk.Label(self, image=imgtk)
        label.image = imgtk
        label.pack()
