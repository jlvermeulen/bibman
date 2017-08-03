import tkinter as tk

from viewsource import ViewSource
import database as db

class FindSource(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)

        entry_frame = tk.Frame(self)
        entry_frame.grid(row = 0, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(entry_frame, 1, weight = 1)

        tk.Label(entry_frame, text = 'Author:').grid(row = 0, column = 0, sticky = 'nesw')
        tk.Label(entry_frame, text = 'Title:').grid(row = 1, column = 0, sticky = 'nesw')

        self.author_entry = tk.Entry(entry_frame)
        self.author_entry.grid(row = 0, column = 1, sticky = 'nesw')

        self.title_entry = tk.Entry(entry_frame)
        self.title_entry.grid(row = 1, column = 1, sticky = 'nesw')

        tk.Button(self, text = 'Search', command = self.search).grid(row = 1, column = 0, sticky = 'nesw')

        self.result_list = tk.Listbox(self, selectmode = 'single')
        self.result_list.grid(row = 2, column = 0, sticky = 'nesw')

        tk.Button(self, text = 'View source', command = self.open).grid(row = 3, column = 0, sticky = 'nesw')

    results = dict()
    def search(self):
        author = self.author_entry.get()
        title  = self.title_entry.get()

        authors = []
        titles  = []

        if author:
            authors = db.query_author(author)
        if title:
            titles = db.query_title(title)

        for result in set().union(authors, titles):
            item = result.list_entry()
            self.results[item] = result
            self.result_list.insert('end', item)

    def open(self):
        for item in self.result_list.curselection():
            ViewSource(self, self.results[self.result_list.get(item)])
