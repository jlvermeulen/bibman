import tkinter as tk

import settings

class ViewSource(tk.Toplevel):
    def __init__(self, parent, source):
        super().__init__(parent)
        super().title(source.list_entry())
        super().geometry(settings.get('view_window_geometry'))

        tk.Label(self, text = 'View source window').pack()

    def destroy(self):
        settings.set('view_window_geometry', super().geometry())
        settings.save()
        super().destroy()
