import tkinter
import threading
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import Parser


root = tkinter.Tk()
root.wm_title("Image Sorter")

landscapes_var = BooleanVar()
portraits_var = BooleanVar()
squares_var = BooleanVar()
subfolders_var = BooleanVar()
structure_var = BooleanVar()
sort_size_var = BooleanVar()

continue_updates = True

size_sorting_options = ["Larger Than", "Smaller Than", "Exactly"]

source_frame = LabelFrame(root, text="Source:")
source_entry = Entry(source_frame)
source_entry.config(state="readonly")

output_frame = LabelFrame(root, text="Messages:")
output_textbox = Text(output_frame, width=29, height=5)

threads = []


def update_output():

    if not continue_updates:
        return

    global output_textbox

    file_number = Parser.file_number
    master_list = Parser.master_list
    portraits_list = Parser.sorted_portraits
    landscapes_list = Parser.sorted_landscapes
    squares_list = Parser.sorted_squares
    bad_list = Parser.bad_files

    output_textbox.delete("1.0", END)
    if not Parser.master_sort_complete:
        output_text = "Analyzing file " + str(file_number) + " of " + str(len(master_list)) + "."
    else:
        output_text = str(file_number) + " of " + str(len(master_list)) + " files analyzed."
    if portraits_list:
        number_of_portraits = str(portraits_list)
        output_text += "\n" + number_of_portraits + " portrait files sorted."
    if landscapes_list:
        number_of_landscapes = str(landscapes_list)
        output_text += "\n" + number_of_landscapes + " landscape files sorted."
    if squares_list:
        number_of_squares = str(squares_list)
        output_text += "\n" + number_of_squares + " square files sorted."
    if (not portraits_list and not landscapes_list and not squares_list) and Parser.sorting_complete:
        output_text += "\nNo files were sorted."
    if bad_list:
        number_of_bads = str(len(bad_list))
        output_text += "\n" + number_of_bads + " files could not be read."

    output_textbox.insert(END, output_text)


def checkbox_option_collector():  # Gather the values of all checkboxes
    return [subfolders_var.get(), structure_var.get(), portraits_var.get(), landscapes_var.get(), squares_var.get(),
            sort_size_var.get()]


def select_source_path():

    Parser.path = filedialog.askdirectory()
    # The following lines will update the Source Entry box with the new path but keep it from being edited
    source_entry.config(state=NORMAL)
    source_entry.delete(0, END)
    source_entry.insert(0, Parser.path)
    source_entry.config(state="readonly")


def sort_button_on_click(size_selection, width_height):

    #  This function ensures a new thread is started each time the sort button is clicked
    #  A thread is required to ensure the GUI does not freeze during lengthy sorts

    local_threads = []

    Parser.continue_sorting = True

    t = threading.Thread(target=Parser.sorter, args=(checkbox_option_collector(), size_selection, width_height)
                         )
    local_threads.append(t)
    threads.append(t)

    for thread in local_threads:
        thread.start()
        while thread.is_alive():    # Pauses the sorting to update the GUI with current status
            sleep(0.5)
            try:
                root.update()
            except TclError:    # This error may be invoked when the application is closed during a sort
                pass
            update_output()


def stop_button_on_click():

    Parser.continue_sorting = False
    Parser.master_sort_complete = True
    Parser.sorting_complete = True


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
                                      onvalue=True, offvalue=False, anchor='w')
    preserve_structure_checkbox = Checkbutton(options_frame, text="Preserve Folder Structure", var=structure_var,
                                              onvalue=True, offvalue=False, anchor='w')

    advanced_sorts_frame = LabelFrame(root, text="Advanced Sorting:")
    sort_size_checkbox = Checkbutton(advanced_sorts_frame, text="Sort by Size", var=sort_size_var,
                                     onvalue=True, offvalue=False)
    width_label = Label(advanced_sorts_frame, text="W:")
    width_entry = Entry(advanced_sorts_frame, width=7)
    height_label = Label(advanced_sorts_frame, text="H:")
    height_entry = Entry(advanced_sorts_frame, width=7)

    browse_button = Button(root, text="Source Folder", command=select_source_path)
    sort_button = Button(root, text="Sort", command=lambda: sort_button_on_click(sort_option_combo.get(),
                                                                                 (width_entry.get(),
                                                                                  height_entry.get()
                                                                                  )
                                                                                 )
                         )
    stop_button = Button(root, text="Stop", command=stop_button_on_click)

    sort_types_frame.grid(column=0, row=0, columnspan=2, sticky=N+S+W+E, padx=4, pady=2)
    landscapes_checkbox.pack(side=LEFT)
    portraits_checkbox.pack(side=LEFT)
    squares_checkbox.pack(side=LEFT)

    options_frame.grid(column=0, row=1, sticky=N+S+W+E, padx=4, pady=2)
    subfolders_checkbox.pack(fill="both")
    preserve_structure_checkbox.pack(fill="both")

    advanced_sorts_frame.grid(column=1, row=1, columnspan=2, sticky=N+S+W+E, padx=4, pady=2)
    sort_size_checkbox.pack()
    sort_option_combo = ttk.Combobox(advanced_sorts_frame, width=15, state="readonly")
    sort_option_combo['values'] = size_sorting_options
    sort_option_combo.set("Larger Than")
    sort_option_combo.pack(padx=4, pady=2)
    width_label.pack(side=LEFT)
    width_entry.pack(side=LEFT, padx=(0,4), pady=2)
    height_label.pack(side=LEFT)
    height_entry.pack(side=LEFT, padx=(0, 4), pady=2)

    browse_button.grid(column=0, row=2, padx=4, pady=2)
    sort_button.grid(column=1, row=2, padx=4, pady=2)
    stop_button.grid(column=2, row=2, padx=4, pady=2)

    source_frame.grid(column=0, row=3, columnspan=3, sticky=N+S+W+E, padx=4, pady=2)
    source_entry.pack(padx=2, pady=2, fill="both")

    output_frame.grid(column=0, row=4, columnspan=3, sticky=N+S+W+E, padx=4, pady=2)
    output_textbox.pack(padx=2, pady=2, fill="both")

    landscapes_checkbox.select()
    portraits_checkbox.select()
    squares_checkbox.select()
    subfolders_checkbox.select()
    preserve_structure_checkbox.select()


def on_exit():

    global continue_updates

    if not Parser.sorting_complete:
        if tkinter.messagebox.askokcancel("Sort Still Running", "A sort operation is still ongoing.\nAre you sure you "
                                                                "wish to exit?"):
            pass
        else:
            return

    Parser.continue_sorting = False
    continue_updates = False
    root.destroy()
