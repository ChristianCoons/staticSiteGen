import unittest
from textnode import TextNode, TextType
from markdown_functions import *

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

class TestMarkdownExtract(unittest.TestCase):
    def test_extract_single_image(self):
        text = "![alt text](image.jpg)"
        expected = [("alt text", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_multiple_images(self):
        text = "![img1](url1.jpg) some text ![img2](url2.jpg)"
        expected = [("img1", "url1.jpg"), ("img2", "url2.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_image_empty_alt(self):
        text = "![](image.jpg)"
        expected = [("", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_single_link(self):
        text = "[link text](https://example.com)"
        expected = [("link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_multiple_links(self):
        text = "[link1](url1.com) text [link2](url2.com)"
        expected = [("link1", "url1.com"), ("link2", "url2.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_empty_link_text(self):
        text = "[](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_mixed_links_and_images(self):
        text = "![img](img.jpg) [link](url.com)"
        self.assertEqual(extract_markdown_images(text), [("img", "img.jpg")])
        self.assertEqual(extract_markdown_links(text), [("link", "url.com")])
    
    def test_no_matches(self):
        text = "Plain text without any markdown links or images"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])
    
    def test_complex_urls(self):
        text = "[complex](https://example.com/path?param=value#fragment)"
        expected = [("complex", "https://example.com/path?param=value#fragment")]
        self.assertEqual(extract_markdown_links(text), expected)



class TestSplitNodesDelimiter(unittest.TestCase):
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

class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for i in range(len(nodes)):
            self.assertEqual(nodes[i].text, expected[i].text)
            self.assertEqual(nodes[i].text_type, expected[i].text_type)
            self.assertEqual(nodes[i].url, expected[i].url)
    
    def test_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)
        
    def test_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        
    def test_italic_only(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        
    def test_code_only(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        
    def test_link_only(self):
        text = "This is a [link](https://boot.dev) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.LINKS)
        self.assertEqual(nodes[1].url, "https://boot.dev")
        
    def test_image_only(self):
        text = "This is an ![image](https://example.com/img.jpg) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(nodes[1].url, "https://example.com/img.jpg")
        
    def test_multiple_same_type(self):
        text = "**Bold1** normal **Bold2**"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text_type, TextType.NORMAL)
        self.assertEqual(nodes[2].text_type, TextType.BOLD)
        
    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)

    def test_basic_blocks(self):
        markdown = """# Heading

This is a paragraph with **bold** and *italic* text.

* List item 1
* List item 2"""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "This is a paragraph with **bold** and *italic* text.")
        self.assertEqual(blocks[2], "* List item 1\n* List item 2")
        
    def test_empty_blocks_removed(self):
        markdown = """# Heading



This is a paragraph."""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "This is a paragraph.")
        
    def test_whitespace_stripped(self):
        markdown = """   # Heading with spaces   

    This paragraph has indentation.    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "# Heading with spaces")
        self.assertEqual(blocks[1], "This paragraph has indentation.")
        
    def test_single_block(self):
        markdown = "Just one block."
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "Just one block.")
        
    def test_empty_string(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
        
    def test_only_whitespace(self):
        markdown = "   \n\n  \n  "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
        
    def test_complex_document(self):
        markdown = """# Main Heading

## Subheading

First paragraph
with multiple lines.

* List item 1
* List item 2
  * Nested item

```python
def hello():
    print("Hello")
```

Final paragraph."""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 6)
        self.assertEqual(blocks[0], "# Main Heading")
        self.assertEqual(blocks[1], "## Subheading")
        self.assertEqual(blocks[2], "First paragraph\nwith multiple lines.")
        self.assertEqual(blocks[3], "* List item 1\n* List item 2\n  * Nested item")
        self.assertEqual(blocks[4], "```python\ndef hello():\n    print(\"Hello\")\n```")
        self.assertEqual(blocks[5], "Final paragraph.")

    def test_mtb_paragraph(self):
        text = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_mtb_empty_block(self):
        self.assertEqual(block_to_block_type(""), "paragraph")

    def test_mtb_headings(self):
        # Test all heading levels
        for i in range(1, 7):
            text = f"{'#' * i} Heading {i}"
            self.assertEqual(block_to_block_type(text), "heading")
        
        # Test invalid heading formats
        self.assertEqual(block_to_block_type("#Invalid heading"), "paragraph")
        self.assertEqual(block_to_block_type("##No space"), "paragraph")

    def test_mtb_code(self):
        # Basic code block
        text = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(text), "code")
        
        # Code block with language specified
        text = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(text), "code")
        
        # Invalid code blocks
        self.assertEqual(block_to_block_type("```\nUnclosed code block"), "paragraph")
        self.assertEqual(block_to_block_type("`Single backtick`"), "paragraph")

    def test_mtb_quote(self):
        # Single line quote
        self.assertEqual(block_to_block_type(">This is a quote"), "quote")
        
        # Multi-line quote
        text = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_block_type(text), "quote")
        
        # Invalid quote (missing > on second line)
        text = ">First line\nSecond line"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_mtb_unordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("* Single item"), "unordered_list")
        self.assertEqual(block_to_block_type("- Single item"), "unordered_list")
        
        # Multiple items
        text = "* First item\n* Second item\n* Third item"
        self.assertEqual(block_to_block_type(text), "unordered_list")
        
        # Mixed * and -
        text = "* First item\n- Second item"
        self.assertEqual(block_to_block_type(text), "unordered_list")
        
        # Invalid list (missing space after *)
        self.assertEqual(block_to_block_type("*Invalid item"), "paragraph")

    def test_mtb_ordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("1. Single item"), "ordered_list")
        
        # Multiple items
        text = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(text), "ordered_list")
        
        # Invalid ordered list (wrong numbering)
        text = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(text), "paragraph")
        
        # Invalid ordered list (missing space after number)
        self.assertEqual(block_to_block_type("1.Invalid item"), "paragraph")
        

if __name__ == '__main__':
    unittest.main()