#! /usr/bin/env python3

from tkinter import ttk
import tkinter as tk

import database as db
from addsource import AddSource
from findsource import FindSource
from exportbibtex import ExportBibtex
import settings

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
        self.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        self.tabs = ttk.Notebook(self)

        self.add_source_frame    = AddSource(self)
        self.find_source_frame   = FindSource(self)
        self.export_bibtex_frame = ExportBibtex(self)

        self.tabs.add(self.add_source_frame, text = 'Add source')
        self.tabs.add(self.find_source_frame, text = 'Find source')
        self.tabs.add(self.export_bibtex_frame, text = 'Generate .bib')

        self.tabs.pack(fill = 'both', expand = 1)

    def destroy(self):
        settings.set('main_window_geometry', self._nametowidget(self.winfo_parent()).geometry())
        settings.save()
        super().destroy()

def main():
    root = tk.Tk()

    settings.load()
    root.geometry(settings.get('main_window_geometry'))

    app = MainWindow(root)

    db.init()
    root.mainloop()

profile = False
if __name__ == '__main__':
    if profile:
        cProfile.run('main()')
    else:
        main()
