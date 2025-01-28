import unittest
from textnode import TextNode, TextType
from split_node_delimiter import split_node_delimiter

class test_splitnodedelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.NORMAL)
        new_nodes = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.NORMAL)
        new_nodes = split_node_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code`", TextType.NORMAL)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_no_split_different_type(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_node_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_unclosed_delimiter(self):
        node = TextNode("This is *unclosed", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_node_delimiter([node], "*", TextType.ITALIC)

    def test_empty_delimiter_sections(self):
        node = TextNode("This has an **** empty bold", TextType.NORMAL)
        new_nodes = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This has an ")
        self.assertEqual(new_nodes[1].text, " empty bold")

if __name__ == '__main__':
    unittest.main()