import tkinter as tk

class ExportBibtex(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text = 'Export Frame', bg = 'green').pack(fill = 'both', expand = 1)
