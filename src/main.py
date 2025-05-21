import os
import shutil
from textnode import TextNode, TextType

def main():
    copy_source_contents()

def copy_source_contents():
    source_directory = "static"
    destination_directory = "public"
    clear_destination_directory(destination_directory)
    copy_contents(source_directory, destination_directory)

def clear_destination_directory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
        os.mkdir(directory, mode=0o777)
    else:
        os.mkdir(destination_directory, mode=0o777)

def copy_contents(source_directory, destination_directory):
    paths_list = os.listdir(source_directory)
    for path in paths_list:
        source_path = os.path.join(source_directory, path)
        destination_path = os.path.join(destination_directory, path)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_contents(source_path, destination_path)

main()