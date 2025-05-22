import os
import shutil
import sys
from textnode import TextNode, TextType
from markdown_parser import *

def main():
    copy_source_contents()
    basepath = get_base_path()
    generate_pages_recursive("content", "template.html", "docs", basepath)

def get_base_path():
    if len(sys.argv) > 0:
        return sys.argv[1]
    return "/"

def copy_source_contents():
    source_directory = "static"
    destination_directory = "docs"
    clear_destination_directory(destination_directory)
    copy_contents(source_directory, destination_directory)

def clear_destination_directory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
        os.mkdir(directory, mode=0o777)
    else:
        os.mkdir(directory, mode=0o777)

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

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with(open(from_path, 'r') as markdown_file):
        markdown_content = markdown_file.read()
    with(open(template_path, 'r') as template_file):
        template_content = template_file.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title_string = extract_title(markdown_content)
    template_content = template_content.replace(f"{{{{ Title }}}}", title_string)
    template_content = template_content.replace(f"{{{{ Content }}}}", html_string)
    template_content = template_content.replace("href=\"/", f"href=\"{base_path}")
    template_content = template_content.replace("src=\"/", f"src=\"{base_path}")
    create_directory_if_nonexistent(dest_path)
    with(open(dest_path, 'w') as html_file):
        html_file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    found_html_paths = find_html_files(dir_path_content)
    for html_file_path in found_html_paths:
        destination_file_path = html_file_path.replace(dir_path_content, dest_dir_path).replace(".md", ".html")
        generate_page(html_file_path, template_path, destination_file_path, base_path)

def find_html_files(start_directory):
    paths_list = os.listdir(start_directory)
    html_paths = []
    for path in paths_list:
        full_path = os.path.join(start_directory, path)
        if os.path.isfile(full_path) and full_path.endswith(".md"):
            html_paths.append(full_path)
        elif os.path.isdir(full_path):
            html_paths.extend(find_html_files(full_path))
    return html_paths

def create_directory_if_nonexistent(path):
    split_path = path.split("/")
    if len(split_path) > 1:
        split_path = split_path[:-1]
    else:
        return
    current_path = ""
    for section in split_path:
        current_path = f"{current_path}{section}"
        if not os.path.isdir(current_path):
            os.mkdir(current_path, mode=0o777)
        current_path = f"{current_path}/"

main()