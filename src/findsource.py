import tkinter as tk

from viewsource import ViewSource
import database as db

class FindSource(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)

        input_frame = tk.Frame(self)
        input_frame.grid(row = 0, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(input_frame, 1, weight = 1)

        tk.Label(input_frame, text = 'Author:').grid(row = 0, column = 0, sticky = 'nsw')
        tk.Label(input_frame, text = 'Title:').grid(row = 1, column = 0, sticky = 'nsw')
        tk.Label(input_frame, text = 'Keyword:').grid(row = 2, column = 0, sticky = 'nsw')

        self.author_input = tk.Entry(input_frame)
        self.author_input.grid(row = 0, column = 1, sticky = 'nesw')

        self.title_input = tk.Entry(input_frame)
        self.title_input.grid(row = 1, column = 1, sticky = 'nesw')

        self.keyword_input = tk.Entry(input_frame)
        self.keyword_input.grid(row = 2, column = 1, sticky = 'nesw')

        tk.Button(self, text = 'Search', command = self.search).grid(row = 1, column = 0, sticky = 'nesw')

        self.result_list = tk.Listbox(self, selectmode = 'single')
        self.result_list.grid(row = 2, column = 0, sticky = 'nesw')

        tk.Button(self, text = 'View source', command = self.open).grid(row = 3, column = 0, sticky = 'nesw')

    results = dict()
    def search(self):
        author  = self.author_input.get()
        title   = self.title_input.get()
        keyword = self.keyword_input.get()

        authors  = []
        titles   = []
        keywords = []

        if author:
            authors = db.query_author(author)
        if title:
            titles = db.query_title(title)
        if keyword:
            keywords = db.query_keyword(keyword)

        self.result_list.delete(0, 'end')
        for result in set().union(authors, titles, keywords):
            item = result.list_entry()
            self.results[item] = result
            self.result_list.insert('end', item)

    def open(self):
        for item in self.result_list.curselection():
            ViewSource(self, self.results[self.result_list.get(item)])
