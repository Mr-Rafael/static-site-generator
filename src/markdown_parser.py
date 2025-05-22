import re
from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node(old_node, delimiter, text_type))
    return new_nodes
    
def split_single_node(old_node, delimiter, text_type):
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    new_texts = old_node.text.split(delimiter)
    if len(new_texts) % 2 != 1:
        raise ValueError(f"Invalid Markdown syntax: The text in this node has an odd number of {delimiter} delimiters.")
    new_nodes = []
    for i in range(0, len(new_texts)):
        if i % 2 == 0:
            new_nodes.append(TextNode(new_texts[i], TextType.TEXT))
        else:
            new_nodes.append(TextNode(new_texts[i], text_type))
    return remove_empty_nodes(new_nodes)

def remove_empty_nodes(nodes_list):
    result_nodes = []
    for node in nodes_list:
        if len(node.text) > 0:
            result_nodes.append(node)
    return result_nodes

def remove_empty_strings(string_list):
    result_strings = []
    for stringe in string_list:
        if len(stringe) > 0:
            result_strings.append(stringe)
    return result_strings

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?:^|[^!])\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node_by_images(old_node))
    return remove_empty_nodes(new_nodes)

def split_single_node_by_images(old_node):
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    link_tuples = extract_markdown_images(old_node.text)
    if len(link_tuples) <= 0:
        return [old_node]
    new_nodes = []
    current_text = old_node.text
    for link_tuple in link_tuples:
        delimiter = f"![{link_tuple[0]}]({link_tuple[1]})"
        split_text = current_text.split(delimiter)
        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        new_nodes.append(TextNode(link_tuple[0], TextType.IMAGE, link_tuple[1] ))
        current_text = split_text[1]
    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(split_single_node_by_links(old_node))
    return remove_empty_nodes(new_nodes)

def split_single_node_by_links(old_node):
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    link_tuples = extract_markdown_links(old_node.text)
    if len(link_tuples) <= 0:
        return [old_node]
    new_nodes = []
    current_text = old_node.text
    for link_tuple in link_tuples:
        delimiter = f"[{link_tuple[0]}]({link_tuple[1]})"
        split_text = current_text.split(delimiter)
        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1] ))
        current_text = split_text[1]
    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def parse_inline_markdown_text(text):

    result_nodes = [TextNode(text, TextType.TEXT)]
    result_nodes = split_nodes_delimiter(result_nodes, "**", TextType.BOLD)
    result_nodes = split_nodes_delimiter(result_nodes, "_", TextType.ITALIC)
    result_nodes = split_nodes_delimiter(result_nodes, "`", TextType.CODE)
    result_nodes = split_nodes_image(result_nodes)
    result_nodes = split_nodes_link(result_nodes)

    return result_nodes

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    block_strings = map(lambda x : x.strip(), block_strings)
    return remove_empty_strings(block_strings)

def block_to_block_type(markdown):
    if re.search('^#{1,6} .*', markdown):
        return BlockType.HEADING
    if re.search('^```\n([^`])*\n```$', markdown):
        return BlockType.CODE
    if check_every_line_starts_with(markdown, '>'):
        return BlockType.QUOTE
    if check_every_line_starts_with(markdown, '-'):
        return BlockType.UNORDERED_LIST
    if check_if_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def check_every_line_starts_with(text, character):
    text_lines = text.split("\n")
    for line in text_lines:
        if line[0] != character:
            return False
    return True

def check_if_ordered_list(text):
    text_lines = text.split("\n")
    for i in range(0, len(text_lines)):
        results = re.search(r"(\d+).*", text_lines[i])
        if results is None:
            return False
        if int(results.group(1)) != i + 1:
            return False
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = create_html_node(block, block_type)
        return_nodes.append(html_node)
    return ParentNode(tag="div", children=return_nodes)

def create_html_node(text, type):
    match type:
        case BlockType.HEADING:
            heading_level = get_heading_level(text)
            return LeafNode(tag=f"h{heading_level}", value=text[heading_level + 1:])
        case BlockType.CODE:
            child_node = LeafNode(tag="code", value=text[4:-3])
            return ParentNode(tag="pre", children=[child_node])
        case BlockType.QUOTE:
            quote_text = get_quote_text(text)
            return LeafNode(tag="blockquote", value=quote_text)
        case BlockType.UNORDERED_LIST:
            line_nodes = get_unordered_list_leaves(text)
            return ParentNode(tag="ul", children=line_nodes)
        case BlockType.ORDERED_LIST:
            line_nodes = get_ordered_list_leaves(text)
            return ParentNode(tag="ol", children=line_nodes)
        case BlockType.PARAGRAPH:
            paragraph = parse_paragraph(text)
            return paragraph

def parse_paragraph(text):
    text_nodes = parse_inline_markdown_text(text)
    html_nodes = list(map(lambda x: TextNode.textnode_to_html_node(x), text_nodes))
    return ParentNode(tag="p", children=html_nodes)

def get_heading_level(markdown):
    for i in range(0,6):
        if markdown[i] != '#':
            return i

def get_quote_text(markdown):
    lines = markdown[2:].split("\n>")
    return "\n".join(lines)

def get_unordered_list_leaves(markdown):
    lines = markdown[2:].split("\n- ")
    unordered_list_nodes = []
    for line in lines:
        unordered_list_nodes.append(get_list_element(line))
    return unordered_list_nodes

def get_ordered_list_leaves(markdown):
    lines = remove_empty_strings(re.split(r"\n*\d+. ", markdown))
    ordered_list_nodes = []
    for line in lines:
        ordered_list_nodes.append(get_list_element(line))
    return ordered_list_nodes

def get_list_element(text):
    text_nodes = parse_inline_markdown_text(text)
    html_nodes = list(map(lambda x: TextNode.textnode_to_html_node(x), text_nodes))
    return ParentNode(tag="li", children=html_nodes)

def extract_title(markdown):
    title_match = re.findall(r"^#\s*(.*)\n", markdown)
    if len(title_match) < 1:
        raise ValueError("The file submitted does not have a title.")
    return title_match[0].strip()

def get_nodes_string(text_nodes):
    return_string = ""
    for text_node in text_nodes:
        if text_node.text_type == TextType.IMAGE or text_node.text_type == TextType.LINK:
            return_string += f"- {text_node.text_type.value}: |{text_node.text}| --> {text_node.url}\n"
        else:
            return_string += f"- {text_node.text_type.value}: |{text_node.text}|\n"
    return return_string