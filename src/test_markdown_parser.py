import unittest

from markdown_parser import *
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):

    def test_text_only(self):
        expected_nodes = [
            TextNode("This is text without delimiters.", TextType.TEXT)
        ]
        test_node = TextNode("This is text without delimiters.", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(expected_nodes[0].text, result_nodes[0].text)
        self.assertEqual(expected_nodes[0].text_type, result_nodes[0].text_type)

    def text_non_text_node(self):
        test_node = TextNode("This is a BOLD node, not text.", TextType.BOLD)
        self.assertRaises(ValueError, split_nodes_delimiter([test_node], "**", TextType.BOLD))

    def test_text_containing_bold(self):
        expected_nodes = [
            TextNode("This text contains ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(".", TextType.TEXT)
        ]
        test_node = TextNode("This text contains **BOLD**.", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        for i in range(0, len(expected_nodes)):
            self.assertEqual(expected_nodes[i].text, result_nodes[i].text)
            self.assertEqual(expected_nodes[i].text_type, result_nodes[i].text_type)

    def test_text_containing_italic(self):
        expected_nodes = [
            TextNode("This text contains ", TextType.TEXT),
            TextNode("ITALIC", TextType.ITALIC),
            TextNode(".", TextType.TEXT)
        ]
        test_node = TextNode("This text contains _ITALIC_.", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "_", TextType.ITALIC)
        for i in range(0, len(expected_nodes)):
            self.assertEqual(expected_nodes[i].text, result_nodes[i].text)
            self.assertEqual(expected_nodes[i].text_type, result_nodes[i].text_type)

    def test_text_containing_code(self):
        expected_nodes = [
            TextNode("Look at my code:\n", TextType.TEXT),
            TextNode("CODE\nMORE CODE", TextType.CODE),
            TextNode("\nPretty neat, huh?", TextType.TEXT)
        ]
        test_node = TextNode("Look at my code:\n`CODE\nMORE CODE`\nPretty neat, huh?", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "`", TextType.CODE)
        for i in range(0, len(expected_nodes)):
            self.assertEqual(expected_nodes[i].text, result_nodes[i].text)
            self.assertEqual(expected_nodes[i].text_type, result_nodes[i].text_type)

    def test_delimiter_at_the_end(self):
        expected_nodes = [
            TextNode("This text ends in ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD)
        ]
        test_node = TextNode("This text ends in **BOLD**", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        for i in range(0, max(len(expected_nodes), len(result_nodes))):
            self.assertEqual(expected_nodes[i].text, result_nodes[i].text)
            self.assertEqual(expected_nodes[i].text_type, result_nodes[i].text_type)

    def test_mixed_delimiters(self):
        expected_nodes = [
            TextNode("This text contains ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("ITALIC", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("CODE", TextType.CODE),
            TextNode(".", TextType.TEXT)
        ]
        test_node = TextNode("This text contains **BOLD**, _ITALIC_ and `CODE`.", TextType.TEXT)
        result_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        result_nodes = split_nodes_delimiter(result_nodes, "_", TextType.ITALIC)
        result_nodes = split_nodes_delimiter(result_nodes, "`", TextType.CODE)
        for i in range(0, len(expected_nodes)):
            self.assertEqual(expected_nodes[i].text, result_nodes[i].text)
            self.assertEqual(expected_nodes[i].text_type, result_nodes[i].text_type)

    def test_no_closing_delimiter(self):
        test_node = TextNode("This text contains **No closing delimiter", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [test_node], "**", TextType.BOLD)

    def test_extract_images(self):
        expected_tuples = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual_tuples = extract_markdown_images(text)
        self.assertEqual(expected_tuples, actual_tuples)

    def test_extract_links(self):
        expected_tuples = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual_tuples = extract_markdown_links(text)
        self.assertEqual(expected_tuples, actual_tuples)

    def test_extract_links_and_images(self):
        expected_link_tuples = [('to boot dev', 'https://www.boot.dev')]
        expected_image_tuples = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        actual_link_tuples = extract_markdown_links(text)
        actual_image_tuples = extract_markdown_images(text)
        self.assertEqual(expected_link_tuples, actual_link_tuples)
        self.assertEqual(expected_image_tuples, actual_image_tuples)
    
    def test_split_by_images(self):
        expected_nodes = [TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        test_node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        split_text = split_nodes_image([test_node])
        self.assertEqual(expected_nodes, split_text)
    
    def test_split_by_links(self):
        expected_nodes = [TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ]
        test_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        split_text = split_nodes_link([test_node])
        self.assertEqual(expected_nodes, split_text)
    
    def test_split_by_images_and_links(self):
        expected_nodes = [TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(", a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(".", TextType.TEXT)
        ]
        full_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), a link [to boot dev](https://www.boot.dev) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        test_node = TextNode(full_text, TextType.TEXT)
        split_text = split_nodes_link([test_node])
        split_text = split_nodes_image(split_text)
        self.assertEqual(expected_nodes, split_text)

    def test_parse_markdown_text(self):
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        full_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result_nodes = parse_markdown_text(full_text)

        self.assertEqual(expected_nodes, result_nodes)