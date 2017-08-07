import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext

import settings, dialog
import database as db

class ExportBibtex(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        container = tk.Frame(self)
        container.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Grid.columnconfigure(container, 0, weight = 1)
        tk.Grid.rowconfigure(container, 0, weight = 1)

        self.bibtex_output = tkscrolledtext.ScrolledText(container, state = 'disabled')
        self.bibtex_output.grid(row = 0, column = 0, sticky = 'nesw', pady = (0, 2))
        self.bibtex_output.bind('<1>', lambda e: self.bibtex_output.focus_set())

        button_frame = tk.Frame(container)
        button_frame.grid(row = 1, column = 0, sticky = 'nesw', pady = (2, 0))
        tk.Grid.columnconfigure(button_frame, 0, weight = 1, uniform = 'equal')
        tk.Grid.columnconfigure(button_frame, 1, weight = 1, uniform = 'equal')

        tk.Button(button_frame, text = 'Preview BibTeX', command = self.generate_bibliography).grid(row = 0, column = 0, sticky = 'nesw')
        tk.Button(button_frame, text = 'Export to file', command = self.export_to_file).grid(row = 0, column = 1, sticky = 'nesw')

    def generate_bibliography(self):
        self.bibtex_output.config(state = 'normal')
        self.bibtex_output.delete('1.0', 'end')
        for source in db.get_all():
            self.bibtex_output.insert('end', source.bibtex())
            self.bibtex_output.insert('end', '\n')
        self.bibtex_output.config(state = 'disabled')

    def export_to_file(self):
        filename = dialog.browse_export(self)
        if filename:
            self.generate_bibliography()
            with open(filename, 'w') as file:
                file.write(self.bibtex_output.get('1.0', 'end'))
