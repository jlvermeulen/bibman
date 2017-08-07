import tkinter as tk

import settings, dialog
from sourceview import SourceView
import database as db

import os, os.path, subprocess, platform

class ViewSource(tk.Toplevel):
    def __init__(self, parent, source):
        super().__init__(parent)
        self.geometry(settings.get('view_window_geometry'))

        container = tk.Frame(self)
        container.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Grid.columnconfigure(container, 0, weight = 1)
        tk.Grid.rowconfigure(container, 0, weight = 1)

        self.sourceview = SourceView(container)
        self.sourceview.grid(row = 0, column = 0, sticky = 'nesw')

        button_frame = tk.Frame(container)
        button_frame.grid(row = 1, column = 0, sticky = 'nesw')
        for x in range(0, 4):
            tk.Grid.columnconfigure(button_frame, x, weight = 1, uniform = 'equal')

        tk.Button(button_frame, text = 'Save changes', command = self.save_changes).grid(row = 0, column = 0, sticky = 'nesw')
        tk.Button(button_frame, text = 'View PDF', command = self.view_pdf).grid(row = 0, column = 1, sticky = 'nesw')
        tk.Button(button_frame, text = 'Remove entry', command = self.delete).grid(row = 0, column = 2, sticky = 'nesw')
        tk.Button(button_frame, text = 'Close', command = self.destroy).grid(row = 0, column = 3, sticky = 'nesw')

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

    def delete(self):
        confirmed = dialog.confirm_deletion(self, 1)
        if confirmed == 'no':
            return

        db.session.delete(self.source)
        db.session.commit()
        self.destroy()

    def destroy(self):
        settings.set('view_window_geometry', super().geometry())
        settings.save()
        super().destroy()
