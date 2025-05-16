import re
from textnode import TextType, TextNode

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
    matches = re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
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

def get_nodes_string(text_nodes):
    return_string = ""
    for text_node in text_nodes:
        if text_node.text_type == TextType.IMAGE or text_node.text_type == TextType.LINK:
            return_string += f"- {text_node.text_type.value}: |{text_node.text}| --> {text_node.url}\n"
        else:
            return_string += f"- {text_node.text_type.value}: |{text_node.text}|\n"
    return return_string