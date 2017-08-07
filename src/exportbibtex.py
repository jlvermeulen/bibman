import tkinter as tk

class ExportBibtex(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        container = tk.Frame(self)
        container.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Label(container, text = 'Export Frame').pack(fill = 'both', expand = 1)
