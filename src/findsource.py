import tkinter as tk

from viewsource import ViewSource
import database as db
import dialog

class FindSource(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        container = tk.Frame(self)
        container.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Grid.columnconfigure(container, 0, weight = 1)
        tk.Grid.rowconfigure(container, 2, weight = 1)

        input_frame = tk.Frame(container)
        input_frame.grid(row = 0, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(input_frame, 1, weight = 1)

        tk.Label(input_frame, text = 'Author:').grid(row = 0, column = 0, sticky = 'nsw')
        tk.Label(input_frame, text = 'Title:').grid(row = 1, column = 0, sticky = 'nsw')
        tk.Label(input_frame, text = 'Keyword:').grid(row = 2, column = 0, sticky = 'nsw')

        self.author_input = tk.Entry(input_frame)
        self.author_input.grid(row = 0, column = 1, sticky = 'nesw', pady = (0, 2))
        self.author_input.bind('<Return>', lambda x: self.search())

        self.title_input = tk.Entry(input_frame)
        self.title_input.grid(row = 1, column = 1, sticky = 'nesw', pady = 2)
        self.title_input.bind('<Return>', lambda x: self.search())

        self.keyword_input = tk.Entry(input_frame)
        self.keyword_input.grid(row = 2, column = 1, sticky = 'nesw', pady = 2)
        self.keyword_input.bind('<Return>', lambda x: self.search())

        tk.Button(container, text = 'Search', command = self.search).grid(row = 1, column = 0, sticky = 'nesw', pady = 2)

        self.result_list = tk.Listbox(container, selectmode = 'extended')
        self.result_list.grid(row = 2, column = 0, sticky = 'nesw')
        self.result_list.bind('<Return>', lambda x: self.view_selection())
        self.result_list.bind('<Delete>', lambda x: self.delete_selection())

        button_frame = tk.Frame(container)
        button_frame.grid(row = 3, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(button_frame, 0, weight = 1, uniform = 'equal')
        tk.Grid.columnconfigure(button_frame, 1, weight = 1, uniform = 'equal')

        tk.Button(button_frame, text = 'View source', command = self.view_selection).grid(row = 0, column = 0, sticky = 'nesw', pady = (2, 0))
        tk.Button(button_frame, text = 'Delete selection', command = self.delete_selection).grid(row = 0, column = 1, sticky = 'nesw', pady = (2, 0))

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

        if not author and not title and not keywords:
            authors = db.get_all()

        self.result_list.delete(0, 'end')
        for result in set().union(authors, titles, keywords):
            item = result.list_entry()
            self.results[item] = result
            self.result_list.insert('end', item)

    def view_selection(self):
        for item in self.result_list.curselection():
            source = self.results[self.result_list.get(item)]
            if not source.is_deleted():
                ViewSource(self, source)
            else:
                dialog.source_deleted(self, source)

    def delete_selection(self):
        selection = list(self.result_list.curselection())
        if len(selection) == 0:
            return

        confirmed = dialog.confirm_deletion(self, len(selection))
        if confirmed == 'no':
            return

        selection.sort(reverse = True)
        for item in selection:
            list_item = self.results.pop(self.result_list.get(item))
            db.session.delete(list_item)
            self.result_list.delete(item)

        db.session.commit()
