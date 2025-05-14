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