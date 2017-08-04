import tkinter as tk

import database as db
from sourcebase import SourceBase

class AddSource(SourceBase):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Button(self, text = 'Add source', command = self.add_source).grid(row = 3, column = 0, sticky = 'nesw')

    def add_source(self):
        source = db.Source()
        self.update_source(source)
        db.session.add(source)
        db.session.commit()
