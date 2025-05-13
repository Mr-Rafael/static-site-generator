import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        test_node = HTMLNode(tag="tag", value="value")
        self.assertRaises(NotImplementedError,test_node.to_html)

    def test_props_to_html(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_string = ' href="https://www.google.com" target="_blank"'

        test_node = HTMLNode(tag="tag", value="value", children="children", props=test_props)
        self.assertEqual(test_node.props_to_html(), expected_string)

    def test_props_to_html_empty(self):
        expected_string = ""

        test_node = HTMLNode(tag="tag", value="value", children="children")
        self.assertEqual(test_node.props_to_html(), expected_string)

    def test_repr(self):
        test_props = {
            "href": "www",
            "target": "blank",
        }
        sub_node_1 = HTMLNode(tag="b", value="test")
        sub_node_2 = HTMLNode(tag="c", value="test")
        test_node = HTMLNode(tag="a", value="testo", children=[sub_node_1, sub_node_2], props=test_props)
        
        self.assertIn("HTML Node:", f"{test_node}")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_tagless_leaf(self):
        test_value = "paragraph"
        node = LeafNode(value=test_value)
        self.assertEqual(node.to_html(), test_value)

    def test_valueless_leaf(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="tag")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )