from textnode import *

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



