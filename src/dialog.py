from tkinter import messagebox
import tkinter.filedialog as filedialog

import settings

import os.path

def confirm_deletion(owner, number):
    template = 'You are about to delete {} source{} from the database. This action cannot be undone. Continue?'
    return messagebox.askquestion(
                'Delete sources',
                template.format('this' if number == 1 else number, 's' if number > 1 else ''),
                icon = 'warning',
                parent = owner
            )

def invalid_bibtex(owner):
    messagebox.showerror('Invalid BibTeX', 'Please provide a single valid BibTeX entry.', parent = owner)

def no_title(owner):
    messagebox.showerror('No title', 'A source must have a title.', parent = owner)

def no_author(owner):
    messagebox.showerror('No author', 'A source must have an author.', parent = owner)

def invalid_pdf_file(owner):
    messagebox.showerror('PDF file does not exist', 'Please give a path to an existing PDF file.', parent = owner)

def source_deleted(owner, source):
    messagebox.showerror('Source deleted', '"{}" was deleted from the database and can no longer be viewed.'.format(source.display_title()), parent = owner)

def open_pdf(owner):
    filename = filedialog.askopenfilename(initialdir = settings.get('last_opened_source_dir'), filetypes = [('PDF files', '*.pdf'), ('PDF files', '*.PDF')], parent = owner)
    if filename:
        settings.set('last_opened_source_dir', os.path.dirname(filename))
    return filename

def browse_export(owner):
    last = settings.get('export_file')
    filename = filedialog.asksaveasfilename(initialdir = os.path.dirname(last), initialfile = os.path.basename(last), defaultextension = '.bib', filetypes = [('BibTeX files', '*.bib')], parent = owner)
    if filename:
        settings.set('export_file', filename)
    return filename
