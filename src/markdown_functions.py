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

def markdown_to_blocks(markdown):
    '''
    Input: raw markdown text, where blocks are seperated by 2 lines, \n\n
    Output: list of block strings, with whitespace removed
    '''
    # first we chop it up
    rawBlocks = markdown.split('\n\n')
    blocks = []
    for block in rawBlocks:
        #must get rid of whitepsace
        strippedBlock = block.strip()
        #check to make sure its not now an empty block
        if strippedBlock:
            blocks.append(strippedBlock)
    
    return blocks

def block_to_block_type(markdownBlock):
    '''
    - Headings start with 1-6 # characters, followed by a space and then the heading text.
    - Code blocks must start with 3 backticks and end with 3 backticks.
    - Every line in a quote block must start with a > character.
    - Every line in an unordered list block must start with a * or - character, followed by a space.
    - Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    - If none of the above conditions are met, the block is a normal paragraph.

    paragraph
    heading
    code
    quote
    unordered_list
    ordered_list
    '''
    #Headings start with 1-6 # characters, followed by a space and then the heading text.
    if markdownBlock.startswith(('# ',
    '## ', '### ', '#### ', '##### ', '###### ')):
        return "heading"
    
    #Code blocks must start with 3 backticks and end with 3 backticks.
    if markdownBlock.startswith('```') and markdownBlock.endswith('```'):
        return "code"
    
    #Every line in a quote block must start with a > character.
    lines = markdownBlock.split('\n')
    allLineQuote = True
    
    for line in lines:
        if not line.startswith('>'):
            allLineQuote = False
    if allLineQuote:
        return "quote"
    
    #Every line in an unordered list block must start with a * or - character, followed by a space.
    if all(line.strip().startswith(('* ', '- ')) for line in lines):
        return "unordered_list"
    
    #Every line in an ordered list block must start with 
    #a number followed by a . character and a space. 
    #The number must start at 1 and increment by 1 for each line.
    isOrderedList = True
    i = 1
    for line in lines:
        #print(f"line: {line}, case: {i}. ")
        if not line.startswith(f"{i}. "):
            isOrderedList = False
        i += 1
    if isOrderedList:
        return "ordered_list"
    
    return "paragraph"
