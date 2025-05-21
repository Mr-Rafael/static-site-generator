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

    def test_parse_inline_markdown_text(self):
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
        result_nodes = parse_inline_markdown_text(full_text)

        self.assertEqual(expected_nodes, result_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_heading(self):
        test_heading = "### This is a heading"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.HEADING)
    
    def test_block_to_block_bad_heading(self):
        test_heading = "#This is a bad heading"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        test_heading = "```\nThis is a code block.\nbeep boop\nhello world\n```"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.CODE)
    
    def test_block_to_block_bad_heading(self):
        test_heading = "```This is a code block with syntax errors\nbeep boop i'm dying\ngoodbye world"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.PARAGRAPH)

    def test_block_to_block_quote(self):
        test_heading = ">This is a quote block\n>Don't believe everything you read on the internet\n>-Ronald Reagan"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.QUOTE)
    
    def test_block_to_block_bad_quote(self):
        test_heading = ">This is a quote block with syntax errors\n>Don't believe every quote\n-Ronal Reagan"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.PARAGRAPH)

    def test_block_to_block_unordered_list(self):
        test_heading = "-This is an unordered list\n-item a\n- item b\n- item c"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_bad_unordered_list(self):
        test_heading = "-This is an unordered list with syntax errors\n-item a\n - item b\n- item c"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.PARAGRAPH)

    def test_block_to_block_ordered_list(self):
        test_heading = "1. This is an ordered list\n2. item 2\n3. item 3\n4. item 4"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_bad_ordered_list(self):
        test_heading = "1. This is an ordered list with bad numbering\n2. item 2\n4. item 3\n5. item 4"
        return_type = block_to_block_type(test_heading)
        self.assertEqual(return_type, BlockType.PARAGRAPH)

    def test_parse_heading(self):
        expected_html = "<h3>This is a heading</h3>"
        test_markdown = "### This is a heading"
        test_markdown_type = BlockType.HEADING
        result_node = create_html_node(test_markdown, test_markdown_type)
        result_html = result_node.to_html()
        self.assertEqual(expected_html, result_html)

    def test_parse_code(self):
        expected_html = "<pre><code>This is a code block\nbeep boop\n hello world.\n</code></pre>"
        test_markdown = "```\nThis is a code block\nbeep boop\n hello world.\n```"
        test_markdown_type = BlockType.CODE
        result_node = create_html_node(test_markdown, test_markdown_type)
        result_html = result_node.to_html()
        self.assertEqual(expected_html, result_html)

    def test_parse_quote(self):
        expected_html = "<blockquote>This is a block quote\nDon't trust everything you read on the internet.\n - Calvin Coolidge.</blockquote>"
        test_markdown = ">This is a block quote\n>Don't trust everything you read on the internet.\n> - Calvin Coolidge."
        test_markdown_type = BlockType.QUOTE
        result_node = create_html_node(test_markdown, test_markdown_type)
        result_html = result_node.to_html()
        self.assertEqual(expected_html, result_html)

    def test_parse_unordered_list(self):
        expected_html = "<ul><li>This is an unordered list</li><li>Robots have seen things you people wouldn’t believe.</li><li>Robots are Your Plastic Pal Who’s Fun To Be With.</li></ul>"
        test_markdown = "-This is an unordered list\n-Robots have seen things you people wouldn’t believe.\n-Robots are Your Plastic Pal Who’s Fun To Be With."
        test_markdown_type = BlockType.UNORDERED_LIST
        result_node = create_html_node(test_markdown, test_markdown_type)
        result_html = result_node.to_html()
        self.assertEqual(expected_html, result_html)

    def test_parse_unordered_list(self):
        expected_html = "<ol><li>This is an ordered list</li><li>Robots have shiny metal posteriors which should not be bitten.</li><li>And they have a plan.</li></ol>"
        test_markdown = "1.This is an ordered list\n2.Robots have shiny metal posteriors which should not be bitten.\n3.And they have a plan."
        test_markdown_type = BlockType.ORDERED_LIST
        result_node = create_html_node(test_markdown, test_markdown_type)
        result_html = result_node.to_html()
        self.assertEqual(expected_html, result_html)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
