import os
import os.path
import shutil
from PIL import Image

path = ""

image_file_types = [".jpg", ".jpeg", ".png", ".gif"]

master_list = []
portraits = []
landscapes = []
squares = []
bad_files = []

sorted_portraits = 0
sorted_landscapes = 0
sorted_squares = 0

file_number = 0

master_sort_complete = True
sorting_complete = True
continue_sorting = True


def check_and_create_path(file_path):

    if not os.path.exists(file_path):
        os.makedirs(file_path)


def copy_file(preserve_structure, current_file, full_path):

    folder_structure = ""

    if preserve_structure:
        file_name = current_file.strip(path)  # Removes only the source path, leaving the folder structure intact

        # The following 3 lines remove the file name from the string leaving only the folder structure itself
        split_path = file_name.split("\\")
        del split_path[-1]
        folder_structure = "\\".join(split_path)

    else:
        split_path = current_file.split("\\")
        file_name = "\\" + split_path[-1]  # Gets last item in path, which should be the file name

    check_and_create_path(full_path + folder_structure)
    shutil.copyfile(current_file, full_path + file_name)


def directory_parser(include_subs):

    global master_list

    master_list = []

    for directory_paths, directory_names, file_names in os.walk(path):
        if "Sorted" in directory_paths:
            continue
        for eachType in image_file_types:
            for fileName in [f for f in file_names if f.endswith(eachType)]:
                master_list.append(os.path.join(directory_paths, fileName))
        if not include_subs:
            break


def master_sorter(width, height, current_file):

    if width > height:
        landscapes.append(current_file)
    elif height > width:
        portraits.append(current_file)
    else:
        squares.append(current_file)


def sorter(checkbox_options, size_selection, width_height):

    include_subs, preserve_structure, sort_ports, sort_lands, sort_squares, sort_by_size = checkbox_options
    size_sort_width, size_sort_height = width_height
    size_sort_width = int(size_sort_width)
    size_sort_height = int(size_sort_height)

    directory_parser(include_subs)

    global master_list, portraits, landscapes, squares, bad_files
    global file_number, sorted_portraits, sorted_landscapes, sorted_squares, sorting_complete, master_sort_complete

    master_sort_complete = False
    sorting_complete = False

    sorted_portraits = 0
    sorted_landscapes = 0
    sorted_squares = 0

    file_number = 0

    portraits = []
    landscapes = []
    squares = []
    bad_files = []

    for eachFile in master_list:

        if not continue_sorting:
            return

        file_number += 1
        
        try:
            im = Image.open(eachFile)
        except OSError:
            bad_files.append(eachFile)
            continue

        width, height = im.size

        if sort_by_size:
            if size_selection == "Larger Than":
                if (width > size_sort_width) and (height > size_sort_height):
                    master_sorter(width, height, eachFile)
            elif size_selection == "Smaller Than":
                if (width < size_sort_width) and (height < size_sort_height):
                    master_sorter(width, height, eachFile)
            elif size_selection == "Exactly":
                if (width == size_sort_width) and (height == size_sort_height):
                    master_sorter(width, height, eachFile)
        else:
            master_sorter(width, height, eachFile)

    master_sort_complete = True

    if portraits and sort_ports:

        full_port_path = path + "\\Sorted\\Portraits"

        check_and_create_path(full_port_path)

        for eachFile in portraits:

            if not continue_sorting:
                return

            copy_file(preserve_structure, eachFile, full_port_path)

            sorted_portraits += 1

    if landscapes and sort_lands:

        full_land_path = path + "\\Sorted\\Landscapes"

        if not os.path.exists(full_land_path):
            os.makedirs(full_land_path)

        for eachFile in landscapes:

            if not continue_sorting:
                return

            copy_file(preserve_structure, eachFile, full_land_path)

            sorted_landscapes += 1

    if squares and sort_squares:

        full_square_path = path + "\\Sorted\\Squares"

        if not os.path.exists(full_square_path):
            os.makedirs(full_square_path)

        for eachFile in squares:

            if not continue_sorting:
                return

            copy_file(preserve_structure, eachFile, full_square_path)

            sorted_squares += 1

    sorting_complete = True

