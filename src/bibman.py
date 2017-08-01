#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

import database

import os.path, glob, cProfile

class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.tags = ['title', 'author', 'year', 'entry_type']
        self.tag_data = {}
        for tag in self.tags:
            self.tag_data[tag] = []

        self.parent.title('bibman')
        self.pack(fill = tk.BOTH, expand = 1)

        self.frame = tk.Frame(self)
        self.frame.pack(fill = tk.BOTH, expand = 1)

        self.button = tk.Button(self.frame, text = "Read data", command = self.fill_table)
        self.button.grid(row = 0, column = 0, sticky = 'w')

        self.title_label      = tk.Label(self.frame, text = 'Title:')
        self.author_label     = tk.Label(self.frame, text = 'Author:')
        self.year_label       = tk.Label(self.frame, text = 'Year:')
        self.entry_type_label = tk.Label(self.frame, text = 'Entry type:')

        self.title_label.grid(row = 1, column = 0, sticky = 'w', padx = 10)
        self.author_label.grid(row = 1, column = 1, sticky = 'w', padx = 10)
        self.year_label.grid(row = 1, column = 2, sticky = 'w', padx = 10)
        self.entry_type_label.grid(row = 1, column = 3, sticky = 'w', padx = 10)

    def fill_table(self):
        return
        #self.gather_data(path)
        #self.show_data()
        #database.session.commit()

    def gather_data(self, path):
        self.tracks = []

        for file in glob.glob(os.path.join(path, '*.flac')):
            self.tracks.append(database.Track())

            for tag in self.tags:
                value = metaflac.get_attribute(tag, file)
                self.tag_data[tag].append(value)
                setattr(self.tracks[-1], tag, value)

            database.session.add(self.tracks[-1])

    def show_data(self):
        i = 0
        for tag in self.tags:
            j = 2
            for value in self.tag_data[tag]:
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
