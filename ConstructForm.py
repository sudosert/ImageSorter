import tkinter
from tkinter import *
from tkinter import filedialog
import Parser


root = tkinter.Tk()
root.wm_title("Image Sorter")

landscapes_var = BooleanVar()
portraits_var = BooleanVar()
squares_var = BooleanVar()
subfolders_var = BooleanVar()


def select_path():

    Parser.path = filedialog.askdirectory()


def construct_form():

    sort_types_frame = LabelFrame(root, text="Sort:")
    landscapes_checkbox = Checkbutton(sort_types_frame, text="Landscapes", var=landscapes_var,
                                      onvalue=True, offvalue=False)
    portraits_checkbox = Checkbutton(sort_types_frame, text="Portraits", var=portraits_var,
                                     onvalue=True, offvalue=False)
    squares_checkbox = Checkbutton(sort_types_frame, text="Squares", var=squares_var,
                                   onvalue=True, offvalue=False)

    options_frame = LabelFrame(root, text="Options:")
    subfolders_checkbox = Checkbutton(options_frame, text="Include Subfolders", var=subfolders_var,
                                      onvalue=True, offvalue=False)

    output_frame = LabelFrame(root, text="Output:")
    output_textbox = Text(output_frame, width=29, height=5)

    browse_button = Button(root, text="Source Folder", command=select_path)
    sort_button = Button(root, text="Sort", command=lambda: Parser.parser_with_subs(subfolders_var.get(),
                                                                                    portraits_var.get(),
                                                                                    landscapes_var.get(),
                                                                                    squares_var.get()))

    sort_types_frame.grid(column=0, row=0, columnspan=2, sticky=N+S+W+E, padx=4, pady=2)
    landscapes_checkbox.pack(side=LEFT)
    portraits_checkbox.pack(side=LEFT)
    squares_checkbox.pack(side=LEFT)

    options_frame.grid(column=0, row=1, sticky=N+S+W+E, padx=4, pady=2)
    subfolders_checkbox.pack(side=LEFT)

    browse_button.grid(column=0, row=2, padx=4, pady=2)
    sort_button.grid(column=1, row=2, padx=4, pady=2)

    output_frame.grid(column=0, row=3, columnspan=2, sticky=N+S+W+E, padx=4, pady=2)
    output_textbox.pack(padx=2, pady=2)

    landscapes_checkbox.select()
    portraits_checkbox.select()
    squares_checkbox.select()
    subfolders_checkbox.select()
