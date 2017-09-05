import tkinter as tk

import database as db
import dialog
from sourceview import SourceView

class AddSource(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        container = tk.Frame(self)
        container.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Grid.columnconfigure(container, 0, weight = 1)
        tk.Grid.rowconfigure(container, 0, weight = 1)

        self.sourceview = SourceView(container)
        self.sourceview.grid(row = 0, column = 0, sticky = 'nesw')

        tk.Button(container, text = 'Add source', command = self.add_source).grid(row = 1, column = 0, sticky = 'nesw', pady = (2, 0))

    def add_source(self):
        source = db.Source()
        self.sourceview.update_source(source)

        if db.contains(source):
            dialog.duplicate(self)

        db.session.add(source)
        db.session.commit()
