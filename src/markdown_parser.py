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
    return_nodes = []
    for node in nodes_list:
        if len(node.text) > 0:
            return_nodes.append(node)
    return return_nodes