import unittest
from textnode import *
from text_to_html import * 


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text_conversion(self):
        node = TextNode("Hello, world!", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.to_html(), "Hello, world!")
    
    def test_bold_conversion(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_italic_conversion(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_code_conversion(self):
        node = TextNode("var x = 42", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "var x = 42")
        self.assertEqual(html_node.to_html(), "<code>var x = 42</code>")
    
    def test_link_conversion(self):
        node = TextNode("Click me!", TextType.LINKS, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click me!</a>')
    
    def test_image_conversion(self):
        node = TextNode("Alt text", TextType.IMAGES, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "Alt text"})
        self.assertEqual(html_node.to_html(), '<img src="image.png" alt="Alt text">')
    
    def test_link_without_url_raises_error(self):
        node = TextNode("Click me!", TextType.LINKS)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_image_without_url_raises_error(self):
        node = TextNode("Alt text", TextType.IMAGES)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
