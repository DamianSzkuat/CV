import tkinter as tk
from gui.mainwindow import Ui_mainwindow

# Main window, has to be created first
root = tk.Tk()

# Add windget
mainwindow = Ui_mainwindow(root)

# Window wont appear unlti this is run
root.mainloop()
