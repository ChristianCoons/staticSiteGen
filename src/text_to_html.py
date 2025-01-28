from htmlnode import *
from leafnode import*
from textnode import *


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
            
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
        
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
        
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
        
    elif text_node.text_type == TextType.LINKS:
        if text_node.url is None:
            raise ValueError("Link text node must have a url")
        return LeafNode("a", text_node.text, {"href": text_node.url})
        
    elif text_node.text_type == TextType.IMAGES:
        if text_node.url is None:
            raise ValueError("Image text node must have a url")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
    else:
        raise ValueError(f"Invalid text node type: {text_node.text_type}")