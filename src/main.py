import os
import shutil
from textnode import TextNode, TextType
from markdown_parser import *

def main():
    copy_source_contents()
    generate_page("content/index.md", "template.html", "public/index.html")

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with(open(from_path, 'r') as markdown_file):
        markdown_content = markdown_file.read()
    with(open(template_path, 'r') as template_file):
        template_content = template_file.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title_string = extract_title(markdown_content)
    template_content = template_content.replace(f"{{{{ Title }}}}", title_string)
    template_content = template_content.replace(f"{{{{ Content }}}}", html_string)
    create_directory_if_nonexistent(dest_path)
    with(open(dest_path, 'w') as html_file):
        html_file.write(template_content)

def create_directory_if_nonexistent(path):
    split_path = path.split("/")
    if len(split_path) > 1:
        split_path = split_path[:-1]
    else:
        return
    current_path = ""
    for section in split_path:
        if not os.path.isdir(section):
            os.mkdir(section)
        current_path = f"{section}/"

main()