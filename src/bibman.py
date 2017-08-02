#! /usr/bin/env python3

from tkinter import ttk
import tkinter as tk

import database
from addsource import AddSource
from findsource import FindSource
from exportbibtex import ExportBibtex

import os.path, glob, cProfile, bibtexparser

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
        self.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        self.tabs = ttk.Notebook(self)

        self.add_source_frame    = AddSource(self)
        self.find_source_frame   = FindSource(self)
        self.export_bibtex_frame = ExportBibtex(self)

        self.tabs.add(self.add_source_frame, text = 'Add source')
        self.tabs.add(self.find_source_frame, text = 'Find source')
        self.tabs.add(self.export_bibtex_frame, text = 'Generate .bib')

        self.tabs.pack(fill = 'both', expand = 1)

    def parse_bibtex(self):
        return
        self.parse_data(test_string)
        self.show_data()
        database.session.commit()

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

    def write_bibtex(self):
        return

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
