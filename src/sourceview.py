import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext

import database as db
import dialog

import os, os.path, shutil, bibtexparser

class SourceView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)

        pdf_frame = tk.Frame(self)
        pdf_frame.grid(row = 0, column = 0, sticky = 'nesw', pady = (0, 2))
        tk.Grid.columnconfigure(pdf_frame, 1, weight = 1)

        tk.Label(pdf_frame, text = 'PDF file:').grid(row = 0, column = 0, sticky = 'nesw')

        self.pdf_input = tk.Entry(pdf_frame)
        self.pdf_input.grid(row = 0, column = 1, sticky = 'nesw')

        tk.Button(pdf_frame, text = '...', command = self.browse_pdf).grid(row = 0, column = 2, sticky = 'nesw')

        input_frame = tk.Frame(self)
        input_frame.grid(row = 1, column = 0, sticky = 'nesw', pady = 2)
        tk.Grid.columnconfigure(input_frame, 0, weight = 1)
        tk.Grid.columnconfigure(input_frame, 1, weight = 1)
        tk.Grid.rowconfigure(input_frame, 1, weight = 1)

        tk.Label(input_frame, text = 'BibTeX:').grid(row = 0, column = 0, sticky = 'w')
        tk.Label(input_frame, text = 'Summary:').grid(row = 0, column = 1, sticky = 'w')

        self.bibtex_input = tkscrolledtext.ScrolledText(input_frame)
        self.bibtex_input.grid(row = 1, column = 0, sticky = 'nesw')

        self.summary_input = tkscrolledtext.ScrolledText(input_frame)
        self.summary_input.grid(row = 1, column = 1, sticky = 'nesw')

        keywords_frame = tk.Frame(self)
        keywords_frame.grid(row = 2, column = 0, sticky = 'nesw', pady = 2)
        tk.Grid.columnconfigure(keywords_frame, 1, weight = 1)

        tk.Label(keywords_frame, text = 'Keywords:').grid(row = 0, column = 0, sticky = 'nesw')

        self.keywords_input = tk.Entry(keywords_frame)
        self.keywords_input.grid(row = 0, column = 1, sticky = 'nesw')

    def browse_pdf(self):
        filename = dialog.open_pdf(self)
        if filename:
            self.pdf_input.delete(0, 'end')
            self.pdf_input.insert(0, filename)

    def update_source(self, source):
        bibtex = self.bibtex_input.get('1.0', 'end')
        parsed = bibtexparser.loads(bibtex)
        if len(parsed.entries) != 1:
            dialog.invalid_bibtex(self)
            return -1
        entry = parsed.entries[0]

        if not 'title' in entry:
            dialog.no_title(self)
            return -1

        if not 'author' in entry:
            dialog.no_author(self)
            return -1

        pdf_path = self.pdf_input.get()
        if not os.path.isfile(pdf_path):
            dialog.invalid_pdf_file(self)
            return -1

        for field in db.fields:
            if field in entry:
                setattr(source, field, entry[field])
            else:
                setattr(source, field, None)
        setattr(source, 'entry_type', entry['ENTRYTYPE'])
        setattr(source, 'keywords', self.keywords_input.get())
        setattr(source, 'summary', self.summary_input.get('1.0', 'end'))

        if not os.path.isdir('pdfs'):
            os.makedirs('pdfs')

        file_name = source.pdf_file_name()
        if pdf_path != os.path.abspath(os.path.join('pdfs', file_name)):
            shutil.copyfile(pdf_path, os.path.join('pdfs', file_name))

        return 0

    def clear(self):
        self.pdf_input.delete(0, 'end')
        self.bibtex_input.delete('1.0', 'end')
        self.summary_input.delete('1.0', 'end')
        self.keywords_input.delete(0, 'end')

    def fill(self, pdf, bibtex, summary, keywords):
        self.pdf_input.insert(0, pdf)
        self.bibtex_input.insert('end', bibtex)
        self.summary_input.insert('end', summary)
        self.keywords_input.insert(0, keywords)
