from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(node1, node2):
        return node1.text == node2.text and node1.text_type == node2.text_type and node1.url == node2.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def textnode_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                text_without_newlines = text_node.text.replace("\n", " ")
                return LeafNode(value=text_without_newlines)
            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)
            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text)
            case TextType.LINK:
                link_prop = {"href": text_node.url}
                return LeafNode(tag="a", value=text_node.text, props=link_prop)
            case TextType.IMAGE:
                image_props = {"src": text_node.url, "alt": text_node.text}
                return LeafNode(tag="img", value="", props=image_props)
            case _:
                raise ValueError(f"Failed to convert a textnode of type {text_node.text_type} to html")