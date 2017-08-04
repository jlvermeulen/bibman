from tkinter import messagebox
import tkinter.filedialog as filedialog

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
    return filedialog.askopenfilename(filetypes = [('PDF files', '*.pdf')], parent = owner)
