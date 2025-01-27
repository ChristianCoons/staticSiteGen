import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class test_leafnode(unittest.TestCase):
    def test_basic_leaf_with_tag_and_value(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")
    
    def test_leaf_with_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")
    
    def test_leaf_with_properties(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_none_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
    
    def test_children_is_empty_list(self):
        node = LeafNode("p", "test")
        self.assertEqual(node.children, [])
        
if __name__ == '__main__':
    unittest.main()