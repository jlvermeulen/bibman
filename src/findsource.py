import tkinter as tk

class FindSource(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text = 'Search Frame', bg = 'green').pack(fill = 'both', expand = 1)
