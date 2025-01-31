from textnode import *
import re

def split_node_delimiter(old_nodes, delimiter, text_type):

    newNodes = []
    for oldNode in old_nodes:
        if oldNode.text_type != TextType.NORMAL:
            newNodes.append(oldNode)
        else:
            splitText = oldNode.text.split(delimiter)

            #no delimiter found, split did not split
            if len(splitText) == 1:
                newNodes.append(oldNode)
                continue
            #Unclosed delimiter, must always come in pairs, make the len odd
            elif len(splitText)%2 != 1:
                raise ValueError(f"Unclosed delimiter {delimiter}")
            
            for i in range(len(splitText)):
                text = splitText[i]
                #check for empty delimiter sections, no text
                if text == "":
                    continue

                #We know that even idicies have no delimiters, and are normal,
                #odd indicies have delimiters and are of text_type
                if i%2 == 0:
                    newNodes.append(TextNode(text, TextType.NORMAL))
                else:
                    newNodes.append(TextNode(text, text_type))
    return newNodes

def extract_markdown_images(text):
    #Tuples should contain (alt text, URL)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    """Split text nodes on markdown image syntax."""
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        # Process all image matches
        current_text = old_node.text
        for alt_text, url in images:
            # Split on the full image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)
            
            # Add text before image if it exists
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
            
            # Update remaining text
            if len(parts) > 1:
                current_text = parts[1]
                
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes

def split_nodes_link(old_nodes):
    """Split text nodes on markdown link syntax."""
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        # Process all link matches
        current_text = old_node.text
        for link_text, url in links:
            # Split on the full link markdown
            link_markdown = f"[{link_text}]({url})"
            parts = current_text.split(link_markdown, 1)
            
            # Add text before link if it exists
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINKS, url))
            
            # Update remaining text
            if len(parts) > 1:
                current_text = parts[1]
                
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes

def text_to_textnodes(text):
    firstNode = TextNode(text, TextType.NORMAL)
    newNodes = split_node_delimiter([firstNode], "**", TextType.BOLD)
    newNodes = split_node_delimiter(newNodes, "*", TextType.ITALIC)
    newNodes = split_node_delimiter(newNodes, "`", TextType.CODE)
    newNodes = split_nodes_link(newNodes)
    newNodes = split_nodes_image(newNodes)

    return newNodes




