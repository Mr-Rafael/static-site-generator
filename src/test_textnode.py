import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a link", TextType.BOLD, "url")
        node2 = TextNode("This is a link", TextType.BOLD, "url")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a link", TextType.TEXT)
        node2 = TextNode("This is a link", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a link", TextType.TEXT, "URL")
        node2 = TextNode("This is a link", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a simple text node", TextType.TEXT)
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = "This is a simple text node"
        self.assertEqual(html_node, expected_node)

    def test_bold_type(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = "<b>This is a bold node</b>"
        self.assertEqual(html_node, expected_node)

    def test_italic_type(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = "<i>This is an italic node</i>"
        self.assertEqual(html_node, expected_node)

    def test_code_type(self):
        node = TextNode("This is a\ncode node\nbeep boop", TextType.CODE)
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = "<code>This is a\ncode node\nbeep boop</code>"
        self.assertEqual(html_node, expected_node)
    
    def test_link_type(self):
        node = TextNode("click me", TextType.LINK, "link.com")
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = '<a href="link.com">click me</a>'
        self.assertEqual(html_node, expected_node)
    
    def test_image_type(self):
        node = TextNode("image description", TextType.IMAGE, "pic.png")
        html_node = TextNode.textnode_to_html_node(node).to_html()
        expected_node = '<img src="pic.png" alt="image description"></img>'
        self.assertEqual(html_node, expected_node)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("invalid node", "INVALID")
            TextNode.textnode_to_html_node(node)

if __name__ == "__main__":
    unittest.main()