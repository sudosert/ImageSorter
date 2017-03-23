import os
import os.path
import shutil
from os import listdir
from PIL import Image

path = ""


image_file_types = [".jpg", ".jpeg", ".png", ".gif"]

master_list = []


def sorter(sort_ports, sort_lands, sort_squares):

    global master_list

    portraits = []
    landscapes = []
    squares = []
    bad_files = []

    for eachFile in master_list:
        
        try:
            im = Image.open(eachFile)
        except OSError:
            bad_files.append(eachFile)
            continue

        width, height = im.size

        if width > height:
            landscapes.append(eachFile)
        elif height > width:
            portraits.append(eachFile)
        else:
            squares.append(eachFile)

    if portraits and sort_ports:

        if not os.path.exists(path + "\\" + "Sorted\\Portraits"):
            os.makedirs(path + "\\" + "Sorted\\Portraits")

        for eachFile in portraits:
            split_path = eachFile.split("\\")
            only_file_name = split_path[len(split_path) - 1]
            shutil.copyfile(eachFile, path + "\\" + "Sorted\\Portraits\\" + only_file_name)

        print(str(len(portraits)) + " files sorted into Portraits.")

    if landscapes and sort_lands:

        if not os.path.exists(path + "\\" + "Sorted\\Landscapes"):
            os.makedirs(path + "\\" + "Sorted\\Landscapes")

        for eachFile in landscapes:
            split_path = eachFile.split("\\")
            only_file_name = split_path[len(split_path) - 1]
            shutil.copyfile(eachFile, path + "\\" + "Sorted\\Landscapes\\" + only_file_name)

        print(str(len(landscapes)) + " files sorted into Landscapes.")

    if squares and sort_squares:

        if not os.path.exists(path + "\\" + "Sorted\\Squares"):
            os.makedirs(path + "\\" + "Sorted\\Squares")

        for eachFile in squares:
            split_path = eachFile.split("\\")
            only_file_name = split_path[len(split_path) - 1]
            shutil.copyfile(eachFile, path + "\\" + "Sorted\\Squares\\" + only_file_name)

        print(str(len(squares)) + " files sorted into Squares.")

    if not portraits and not landscapes and not squares:

        print("No files were sorted.")

    if bad_files:

        print(str(len(bad_files)) + " files could not be sorted.")


def parser_with_subs(include_subs, sort_ports, sort_lands, sort_squares):

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

    sorter(sort_ports, sort_lands, sort_squares)
