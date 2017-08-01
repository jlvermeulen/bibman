#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

import bibtexparser

import database

import os.path, glob, cProfile

test_string = '''@article{oliva13,
    author = "Oliva, R. and Pelechano, N.",
    title = "{NEOGEN}: {N}ear optimal generator of navigation meshes for {3D} multi-layered environments",
    journal = "Computers \& Graphics",
    volume = "37",
    number = "5",
    year = "2013",
    pages = "403--412"
}
'''

class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.fields = ['title', 'author', 'year', 'ENTRYTYPE']
        self.entry_data = {}
        for field in self.fields:
            self.entry_data[field] = []

        self.parent.title('bibman')
        self.pack(fill = tk.BOTH, expand = 1)

        self.frame = tk.Frame(self)
        self.frame.pack(fill = tk.BOTH, expand = 1)

        self.parse_button = tk.Button(self.frame, text = "Parse", command = self.parse_bibtex)
        self.parse_button.grid(row = 0, column = 0, sticky = 'w')

        self.export_button = tk.Button(self.frame, text = "Write to BibTeX", command = self.write_bibtex)
        self.export_button.grid(row = 0, column = 1, stick = 'w')

        self.title_label      = tk.Label(self.frame, text = 'Title:')
        self.author_label     = tk.Label(self.frame, text = 'Author:')
        self.year_label       = tk.Label(self.frame, text = 'Year:')
        self.entry_type_label = tk.Label(self.frame, text = 'Entry type:')

        self.title_label.grid(row = 1, column = 0, sticky = 'w', padx = 10)
        self.author_label.grid(row = 1, column = 1, sticky = 'w', padx = 10)
        self.year_label.grid(row = 1, column = 2, sticky = 'w', padx = 10)
        self.entry_type_label.grid(row = 1, column = 3, sticky = 'w', padx = 10)

    def parse_bibtex(self):
        self.parse_data(test_string)
        self.show_data()
        database.session.commit()

    def write_bibtex(self):
        return

    def parse_data(self, bibtex_entry):
        self.sources = []
        self.sources.append(database.Source())

        parsed = bibtexparser.loads(bibtex_entry)
        print(parsed.entries)

        for field in self.fields:
            value = parsed.entries[0][field]
            self.entry_data[field].append(value)
            setattr(self.sources[-1], field, value)

        database.session.add(self.sources[-1])

    def show_data(self):
        i = 0
        for field in self.fields:
            j = 2
            for value in self.entry_data[field]:
                label = tk.Label(self.frame, text = value)
                label.grid(row = j, column = i, sticky = 'w', padx = 10)
                j = j + 1
            i = i + 1

def main():
    root = tk.Tk()
    root.geometry('1280x720+200+200')

    app = MainWindow(root)

    database.init()

    root.mainloop()

profile = False
if __name__ == '__main__':
    if profile:
        cProfile.run('main()')
    else:
        main()
