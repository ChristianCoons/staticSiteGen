import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        

        node = HTMLNode(
            tag="p", 
            value="Example Text", 
            props = {
            "href": "https://www.google.com", 
            "target": "_blank"}
            )
        
        expected = ' href="https://www.google.com" target="_blank"'
        actual = node.props_to_html()

        self.assertEqual(expected, actual)

        # Additional test case for no props
        node_no_props = HTMLNode(
            tag="p",
            value="Example Text"
        )
        self.assertEqual(node_no_props.props_to_html(), "")

        # Additional test case for props not equal
        self.assertNotEqual(node, node_no_props)


if __name__ == '__main__':
    unittest.main()

