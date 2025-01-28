import unittest

from parentnode import *
from leafnode import *


class TestParentNode(unittest.TestCase):
    def test_basic_parent_with_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)
    
    def test_nested_parent_nodes(self):
        inner_parent = ParentNode(
            "div",
            [LeafNode("span", "Inner text")]
        )
        outer_parent = ParentNode(
            "div",
            [
                LeafNode("p", "First"),
                inner_parent,
                LeafNode("p", "Last")
            ]
        )
        expected = "<div><p>First</p><div><span>Inner text</span></div><p>Last</p></div>"
        self.assertEqual(outer_parent.to_html(), expected)
    
    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Text")],
            {"class": "container", "id": "main"}
        )
        # Note: props order might vary, so we'll check parts separately
        result = node.to_html()
        self.assertTrue(result.startswith("<div"))
        self.assertTrue('class="container"' in result)
        self.assertTrue('id="main"' in result)
        self.assertTrue(result.endswith('</div>'))
        self.assertTrue("<p>Text</p>" in result)
    
    def test_no_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Text")])
    
    def test_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
    
    def test_empty_children_list_works(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_deeply_nested_structure(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [LeafNode("p", "Deep text")]
                        )
                    ]
                )
            ]
        )
        expected = "<div><section><article><p>Deep text</p></article></section></div>"
        self.assertEqual(node.to_html(), expected)

if __name__ == '__main__':
    unittest.main()