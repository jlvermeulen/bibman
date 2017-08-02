import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.scrolledtext as tkscrolledtext

class AddSource(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)

        pdf_frame = tk.Frame(self)
        pdf_frame.grid(row = 0, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(pdf_frame, 1, weight = 1)

        tk.Label(pdf_frame, text = 'PDF file:').grid(row = 0, column = 0, sticky = 'nesw')

        self.pdf_entry = tk.Entry(pdf_frame)
        self.pdf_entry.grid(row = 0, column = 1, sticky = 'nesw')

        tk.Button(pdf_frame, text = '...', command = self.browse_pdf).grid(row = 0, column = 2, sticky = 'nesw')

        input_frame = tk.Frame(self)
        input_frame.grid(row = 1, column = 0, sticky = 'nesw')
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
        keywords_frame.grid(row = 2, column = 0, sticky = 'nesw')
        tk.Grid.columnconfigure(keywords_frame, 1, weight = 1)

        tk.Label(keywords_frame, text = 'Keywords:').grid(row = 0, column = 0, sticky = 'nesw')

        self.keywords_entry = tk.Entry(keywords_frame)
        self.keywords_entry.grid(row = 0, column = 1, sticky = 'nesw')

        tk.Button(self, text = 'Add source', command = self.add_source).grid(row = 3, column = 0, sticky = 'nesw')

    def browse_pdf(self):
        filename = tkfiledialog.askopenfilename(filetypes = [('PDF files', '*.pdf')])
        if filename:
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, filename)

    def add_source(self):
        return
