import tkinter as tk

import settings
from sourcebase import SourceBase
import database as db

import os, os.path, subprocess, platform

class ViewSource(tk.Toplevel):
    def __init__(self, parent, source):
        super().__init__(parent)
        self.geometry(settings.get('view_window_geometry'))
        self.config(padx = 5, pady = 5)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 0, weight = 1)

        self.sourceview = SourceBase(self)
        self.sourceview.grid(row = 0, column = 0, sticky = 'nesw')

        button_frame = tk.Frame(self)
        button_frame.grid(row = 1, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(button_frame, 0, weight = 1, uniform = 'equal')
        tk.Grid.columnconfigure(button_frame, 1, weight = 1, uniform = 'equal')
        tk.Grid.columnconfigure(button_frame, 2, weight = 1, uniform = 'equal')

        tk.Button(button_frame, text = 'Save changes', command = self.save_changes).grid(row = 0, column = 0, sticky = 'nsew')
        tk.Button(button_frame, text = 'View PDF', command = self.view_pdf).grid(row = 0, column = 1, sticky = 'nsew')
        tk.Button(button_frame, text = 'Close', command = self.destroy).grid(row = 0, column = 2, sticky = 'nesw')

        self.source = source
        self.load_values()

    def load_values(self):
        self.title(self.source.list_entry())
        self.pdf_path = os.path.abspath(os.path.join('pdfs', self.source.pdf_file_name()))
        self.sourceview.clear()
        self.sourceview.fill(self.pdf_path, self.source.bibtex(), self.source.summary, self.source.keywords)

    def save_changes(self):
        if self.sourceview.update_source(self.source) == -1:
            return
        db.session.commit()
        self.load_values()

    def view_pdf(self):
        system = platform.system()
        if system == 'Linux':
            subprocess.call(['xdg-open', self.pdf_path])
        elif system == 'Windows':
            os.startfile(self.pdf_path)
        elif system == 'Darwin':
            subprocess.call(['open', self.pdf_path])

    def destroy(self):
        settings.set('view_window_geometry', super().geometry())
        settings.save()
        super().destroy()
